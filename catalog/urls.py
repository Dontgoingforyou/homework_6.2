from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts_view, home_view, product_detail, product_list, create_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_view, name='home'),
    path('catalog/', product_list, name='product_list'),
    path('contacts/', contacts_view, name='contacts'),
    path('catalog/<int:pk>/', product_detail, name='product_detail'),
    path('create/', create_product, name='create_product'),
]
