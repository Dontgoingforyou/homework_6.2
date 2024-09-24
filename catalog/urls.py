from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ContactListView, HomeView, ProductDetailView, ProductListView, ProductCreateView, \
    BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactListView.as_view(), name='contacts_list'),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),

    path('blog_list/', BlogPostListView.as_view(), name='blog_list'),
    path('create_blog/', BlogPostCreateView.as_view(), name='create_blog'),
    path('<slug:slug>/update/', BlogPostUpdateView.as_view(), name='update_blog'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='delete_blog'),
    path('<slug:slug>/view/', BlogPostDetailView.as_view(), name='detail_blog'),
]
