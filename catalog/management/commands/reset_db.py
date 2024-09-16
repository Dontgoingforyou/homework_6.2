import os
import django
from django.core.management import BaseCommand
from django.db import connection
from catalog.models import Product

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalog.settings')
django.setup()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print("Отчистка таблицы Product...")

        Product.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1;")

        print("Таблица Product очищена и автоинкремент сброшен.")
