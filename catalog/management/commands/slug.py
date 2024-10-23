from django.core.management.base import BaseCommand
from catalog.models import BlogPost
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Пересохраняет все посты блога для генерации slug'

    def handle(self, *args, **kwargs):
        posts = BlogPost.objects.all()
        for post in posts:
            if not post.slug:
                post.slug = slugify(post.title)
                post.save()
        self.stdout.write(self.style.SUCCESS('Все посты пересохранены'))
