from django.contrib.auth.views import LoginView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, PasswordResetView, CustomLogoutView, UserUpdateView, \
    UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile_update')
]