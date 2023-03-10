from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Post, Tag
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Makind fake posts"

    def handle(self, *args, **kwargs):

        fake = Faker()

        for _ in range(30):
            d = fake.unique
            tag_1 = Tag.objects.create(
                name = d.word()
            )

            tag_2 = Tag.objects.create(
                name = d.word()
            )

            post_1 = Post.objects.create(
                h1=d.sentence(nb_words=4),
                title=d.sentence(nb_words=5),
                description=d.paragraph(nb_sentences=2),
                content=d.paragraph(nb_sentences=10),
                author=User.objects.get(id=1)
            )

            post_1.tags.add(tag_1)
            post_1.tags.add(tag_2)