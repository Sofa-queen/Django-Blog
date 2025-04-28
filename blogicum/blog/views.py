from django.shortcuts import get_object_or_404, render

from blog.constants import POSTS_AMOUNT
from blog.models import Category, Post


def index(request):
    template = 'blog/index.html'
    posts = Post.filter_manager.all()[:POSTS_AMOUNT]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.filter_manager.all(), pk=post_id)
    context = {'post': post}
    template = 'blog/detail.html'
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.post_category.published()
    context = {'category': category,
               'post_list': post_list}
    return render(request, template, context)
