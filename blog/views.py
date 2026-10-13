from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Category, Post

POSTS_PER_PAGE = 5


def post_list(request, category_slug=None):
    posts = Post.published.select_related('author', 'category')
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    query = request.GET.get('q', '').strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

    page = Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {
        'page': page,
        'category': category,
        'query': query,
        'categories': Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status=Post.Status.PUBLISHED))
        ).filter(post_count__gt=0),
    })


def post_detail(request, slug):
    post = get_object_or_404(Post.published.select_related('author', 'category'), slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Thanks! Your comment has been posted.')
            return redirect(post.get_absolute_url() + '#comments')
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': post.comments.filter(approved=True),
        'form': form,
    })
