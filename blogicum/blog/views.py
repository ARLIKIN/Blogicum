import time

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.conf import settings
from django.core.paginator import Paginator

from .models import Post, Category, User


def index(request):
    template = 'blog/index.html'
    page_obj = control_paginator(
        request.GET.get('page'),
        Post.published.order_by('title')
    )
    context = {'page_obj': page_obj}
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
    page_obj = control_paginator(
        request.GET.get('page'),
        category.posts(manager='published').all()
    )
    context = {'page_obj': page_obj, 'category': category}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    page_obj = control_paginator(
        request.GET.get('page'),
        user.posts(manager='published').all()
    )
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, template, context)


def control_paginator(page, list_obj):
    paginator = Paginator(list_obj, settings.ITEM_PER_PAGE)
    return paginator.get_page(page)


def create_post(request):
    template = 'blog/create.html'
    #context = {'profile': user, 'page_obj': paginator}
    #return render(request, template, context)


def add_comment(request, post_id):
    pass


def profile_edit(request):
    pass

def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/404.html', status=405)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)
