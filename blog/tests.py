from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Comment, Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create_user('ahnaf', password='pass12345')
        cls.django = Category.objects.create(name='Django', slug='django')
        cls.python = Category.objects.create(name='Python', slug='python')
        cls.post = Post.objects.create(
            title='Hello Django', slug='hello-django', author=cls.author, category=cls.django,
            body='Django makes web development fast.', status=Post.Status.PUBLISHED,
        )
        cls.draft = Post.objects.create(
            title='Secret draft', slug='secret-draft', author=cls.author, body='Not ready.',
        )
        cls.future = Post.objects.create(
            title='Future post', slug='future-post', author=cls.author, body='Soon.',
            status=Post.Status.PUBLISHED, published_at=timezone.now() + timedelta(days=1),
        )

    def test_list_shows_only_published_posts(self):
        res = self.client.get(reverse('blog:post_list'))
        self.assertContains(res, 'Hello Django')
        self.assertNotContains(res, 'Secret draft')
        self.assertNotContains(res, 'Future post')

    def test_detail_page(self):
        res = self.client.get(self.post.get_absolute_url())
        self.assertContains(res, 'Django makes web development fast.')

    def test_draft_detail_returns_404(self):
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 404)

    def test_category_filter(self):
        Post.objects.create(title='Python tips', slug='python-tips', author=self.author,
                            category=self.python, body='Use venv.', status=Post.Status.PUBLISHED)
        res = self.client.get(reverse('blog:category', args=['python']))
        self.assertContains(res, 'Python tips')
        self.assertNotContains(res, 'Hello Django')

    def test_search(self):
        res = self.client.get(reverse('blog:post_list'), {'q': 'web development'})
        self.assertContains(res, 'Hello Django')
        res = self.client.get(reverse('blog:post_list'), {'q': 'nothing matches'})
        self.assertContains(res, 'No posts found.')

    def test_pagination(self):
        for i in range(6):
            Post.objects.create(title=f'Post {i}', slug=f'post-{i}', author=self.author,
                                body='x', status=Post.Status.PUBLISHED)
        res = self.client.get(reverse('blog:post_list'))
        self.assertEqual(len(res.context['page']), 5)
        self.assertContains(res, 'Page 1 of 2')

    def test_post_comment(self):
        res = self.client.post(self.post.get_absolute_url(), {
            'name': 'Rahim', 'email': 'rahim@example.com', 'body': 'Great post!',
        })
        self.assertRedirects(res, self.post.get_absolute_url() + '#comments', fetch_redirect_response=False)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertContains(self.client.get(self.post.get_absolute_url()), 'Great post!')

    def test_invalid_comment_is_rejected(self):
        res = self.client.post(self.post.get_absolute_url(), {'name': '', 'email': 'bad', 'body': ''})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_hidden_comments_not_shown(self):
        Comment.objects.create(post=self.post, name='Spammer', email='s@example.com', body='spam', approved=False)
        self.assertNotContains(self.client.get(self.post.get_absolute_url()), 'spam')

    def test_reading_minutes(self):
        self.post.body = 'word ' * 600
        self.assertEqual(self.post.reading_minutes, 3)

    def test_seed_command(self):
        call_command('seed_blog', stdout=StringIO())
        self.assertGreaterEqual(Post.published.count(), 7)
