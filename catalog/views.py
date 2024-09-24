from django.core.mail import send_mail
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from catalog.models import Product, Contact, BlogPost

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


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ("name", "description", "image", "category", "purchase_price",)
    success_url = reverse_lazy("catalog:product_list")


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(is_published=True).order_by('-created_at')


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
