from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Имя продукта", help_text="Введите имя продукта"
    )
    description = models.TextField(
        verbose_name="Описание продукта", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="catalog/images",
        verbose_name="Изображение товара",
        help_text="Загрузите изображение товара",
        **NULLABLE
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите название категории",
        related_name="products",
        **NULLABLE
    )
    purchase_price = models.IntegerField(
        verbose_name="Цена за покупку", help_text="Введите цену"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        help_text="Введите дату создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата изменения", help_text="Введите дату изменения", auto_now=True
    )
    manufactured_at = models.DateField(
        verbose_name="Дата производства продукта",
        help_text="Введите дату производства",
        **NULLABLE
    )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Имя категории", help_text="Введите имя категории"
    )
    description = models.TextField(
        verbose_name="Описание категории", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Имя продукта')
    version_number = models.CharField(max_length=50, verbose_name='Номер версии')
    version_name = models.CharField(max_length=150, verbose_name='Имя версии')
    is_current = models.BooleanField(default=False, verbose_name='Актуальная версия')

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"

    def save(self, *args, **kwargs):
        """ Метод устанавливает все остальные версии продуктов как НЕ текущие"""
        if self.is_current:
            Version.objects.filter(product=self.product, is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.version_number


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя", help_text="Введите имя")
    phone = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.name} ({self.phone})"


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок", help_text="Введите заголовок")
    slug = models.CharField(max_length=100, **NULLABLE)
    context = models.TextField(verbose_name="Содержимое", help_text="Введите текст")
    preview_image = models.ImageField(upload_to="catalog/blog_images", verbose_name="Изображение", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", help_text="Введите дату создания")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    class Meta:
        verbose_name = "Запись в блоге"
        verbose_name_plural = "Записи в блоге"

    def __str__(self):
        return self.title
