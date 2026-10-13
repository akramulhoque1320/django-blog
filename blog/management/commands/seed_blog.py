from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from blog.models import Category, Comment, Post

SAMPLE_POSTS = [
    ('Python', 'Getting started with Python virtual environments',
     'Why every Python project deserves its own environment, and how to create one in a minute.',
     'A virtual environment keeps each project\'s dependencies separate.\n\n'
     'Create one with `python -m venv .venv`, activate it, and install packages with pip. '
     'Commit a requirements.txt so others can recreate the same setup.'),
    ('Django', 'Understanding Django models and migrations',
     'Models describe your data; migrations keep the database in sync with them.',
     'In Django every model is a Python class that maps to a database table.\n\n'
     'When you change a model, run `makemigrations` to record the change and `migrate` to apply it.'),
    ('Django', 'Five Django admin tips that save time',
     'list_display, list_filter, search_fields, prepopulated_fields and custom actions.',
     'The Django admin is one of the framework\'s best features.\n\n'
     'Use list_display for useful columns, list_filter and search_fields to find records quickly, '
     'and custom actions to update many rows at once.'),
    ('Career', 'How I organise my developer portfolio',
     'Small, finished, tested projects beat big unfinished ones.',
     'Recruiters skim. A clear README, a live demo and a short feature list go a long way.\n\n'
     'Keep each project focused, write a few tests, and show what you learned.'),
    ('Java', 'Java collections in a nutshell',
     'When to use List, Set and Map, with simple examples.',
     'Use a List when order matters and duplicates are allowed, a Set for unique items, '
     'and a Map to look values up by key.\n\nLinkedHashMap keeps insertion order, which is handy for menus and reports.'),
    ('Python', 'Writing your first unit tests in Python',
     'unittest and pytest make it easy to prove your code works.',
     'Tests give you the confidence to refactor.\n\n'
     'Start with the unittest module from the standard library, then try pytest for shorter tests and fixtures.'),
]


class Command(BaseCommand):
    help = 'Create a demo author, categories, posts and comments.'

    def handle(self, *args, **options):
        User = get_user_model()
        author, created = User.objects.get_or_create(
            username='ahnaf', defaults={'first_name': 'Akramul', 'last_name': 'Hoque'}
        )
        if created:
            author.set_unusable_password()
            author.save()

        now = timezone.now()
        for i, (category_name, title, excerpt, body) in enumerate(SAMPLE_POSTS):
            category, _ = Category.objects.get_or_create(name=category_name, defaults={'slug': slugify(category_name)})
            post, created = Post.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    'title': title,
                    'author': author,
                    'category': category,
                    'excerpt': excerpt,
                    'body': body,
                    'status': Post.Status.PUBLISHED,
                    'published_at': now - timedelta(days=i * 3),
                },
            )
            if created and i == 0:
                Comment.objects.create(post=post, name='Rahim', email='rahim@example.com', body='Very helpful, thanks!')

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(SAMPLE_POSTS)} posts.'))
