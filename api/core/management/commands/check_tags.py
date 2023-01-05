from django.core.management.base import BaseCommand
from core.models import Tag
from django.contrib.auth.models import User
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Makind url for tags if it empty"

    def handle(self, *args, **kwargs):

        tags = Tag.objects.filter(url="")

        for t in tags:
            t.url = slugify(t.name)
            t.save()