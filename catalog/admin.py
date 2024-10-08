from django.contrib import admin
from catalog.models import Product, Category, Contact, BlogPost, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "purchase_price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "context", "preview_image", "created_at", "is_published", "views")


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "version_number", "version_name", "is_current")
