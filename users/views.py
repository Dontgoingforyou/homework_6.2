import secrets
import random
import string

from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Ваш профиль успешно обновлен')
        return super().form_valid(form)


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'users/password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.get(email=email)

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.password = make_password(new_password)
        user.save()
        send_mail(
            subject='Ваш новый пароль',
            message=f'Здравствуйте!\nВаш новый пароль: {new_password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return render(request, 'users/password_reset.html')


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')

    def post(self, request):
        logout(request)
        return redirect('users:login')