import json

from django.core.management import BaseCommand
from catalog.models import Product, Category

json_file = "data.json"


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open(json_file, encoding='utf-8') as file:
            categories = json.load(file)
        return categories

    @staticmethod
    def json_read_products():
        with open(json_file, encoding='utf-8') as file:
            products = json.load(file)
        return products

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            if category['model'] == 'catalog.category':
                category_for_create.append(
                    Category(
                        pk=category["pk"],
                        name=category["fields"]["name"],
                        description=category["fields"]["description"],
                    )
                )
        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            if product['model'] == 'catalog.product':
                product_for_create.append(
                    Product(
                        name=product["fields"]["name"],
                        description=product["fields"]["description"],
                        image=product["fields"].get('image'),
                        category=Category.objects.get(pk=product["fields"].get("category")),
                        purchase_price=product["fields"]["purchase_price"],
                        created_at=product["fields"]["created_at"],
                        updated_at=product["fields"]["updated_at"],
                        manufactured_at=product["fields"]["manufactured_at"],
                    )
                )
        Product.objects.bulk_create(product_for_create)
