from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.conf import settings

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.published.order_by('title')[:settings.POSTS_ON_PAGE]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    postpage = get_object_or_404(Post.published, pk=id)
    context = {'post': postpage, 'show_all': True}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    post_list = get_list_or_404(category.posts(manager='published'))

    context = {'post_list': post_list, 'category': category}
    return render(request, template, context)
