from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts_view, home_view

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_view, name='home'),
    path('contacts/', contacts_view, name='contacts'),
    # path('', home, name='home')
]
