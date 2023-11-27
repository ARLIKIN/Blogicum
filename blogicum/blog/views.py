import datetime as dt

from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Category, User, Comment
from .forms import CommentForm, PostForm


def index(request):
    template = 'blog/index.html'
    page_obj = control_paginator(
        request.GET.get('page'),
        Post.published.order_by('title')
        .filter(pub_date__lte=dt.datetime.now(tz=dt.timezone.utc))
    )
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post_page = get_object_or_404(
        Post.published.all(),
        pk=id
    )
    form = CommentForm()
    comments = post_page.comments.all()
    context = {'post': post_page, 'form': form, 'comments': comments}
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
        user.posts
            .prefetch_related('comments')
            .select_related('location', 'author', 'category')
            .annotate(comment_count=Count('comments'))
    )
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, template, context)


def control_paginator(page, list_obj):
    paginator = Paginator(list_obj, settings.ITEM_PER_PAGE)
    return paginator.get_page(page)


@login_required
def create_post(request):
    template = 'blog/create.html'
    form = PostForm(request.POST or None, request.FILES)
    context = {'form': form}
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(f'profile/{request.user.username}/')
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post.published, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', id=post_id)


def profile_edit(request):
    pass


@login_required
def edit_post(request, post_id):
   pass


def delete_post(request, post_id):
    pass


@login_required
def edit_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    comment = get_object_or_404(Comment, pk=comment_id)
    form = CommentForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = comment.post
        comment.save()
        return redirect('blog:post_detail', id=post_id)
    return render(request, template, context)


def delete_comment(request, post_id, comment_id):
    pass


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/404.html', status=405)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)
