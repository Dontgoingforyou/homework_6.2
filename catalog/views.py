from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Contact, BlogPost, Version

from config import settings


class ContactListView(TemplateView):
    template_name = "catalog/contact_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Contact.objects.all()
        return context


class HomeView(ListView):
    model = Product
    template_name = "catalog/latest_products.html"
    context_object_name = "object_list"
    queryset = Product.objects.order_by('-created_at')[:6]


class ProductListView(ListView):
    model = Product
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            current_version = Version.objects.filter(product=product, is_current=True).first()
            product.current_version = current_version
        return context


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1, can_delete=True)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        form.instance.owner = self.request.user

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1, can_delete=True)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_unpublish_product') and user.has_perm('catalog.can_edit_any_product'):
            return ProductModeratorForm
        raise PermissionDenied('Вы не можете редактировать этот продукт')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.order_by('-created_at')


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        if self.object.views == 100:
            send_mail(
                'Поздравляем! Ваша статья достигла 100 просмотров!',
                f'Ваша статья "{self.object.title}" достигла 100 просмотров! Поздравляем!',
                settings.EMAIL_HOST_USER,
                ['mishael000@yandex.ru'],
                fail_silently=False,
            )
        self.object.save()
        return self.object


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ("title", "slug", "context", "preview_image", "is_published")
    success_url = reverse_lazy("catalog:blog_list")

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save()
            obj.slug = slugify(obj.title)
            obj.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ("title", "slug", "context", "preview_image", "is_published")
    success_url = reverse_lazy("catalog:blog_list")

    def get_success_url(self):
        return reverse('catalog:detail_blog', args=[self.kwargs.get('slug')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("catalog:blog_list")
