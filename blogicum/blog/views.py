import datetime as dt

from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Category, User, Comment
from .forms import CommentForm, PostForm, ProfileForm


def index(request):
    template = 'blog/index.html'
    page_obj = control_paginator(
        request.GET.get('page'),
        Post.published.all()
    )
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post_page = get_object_or_404(
        Post.objects.select_related('location', 'author', 'category'),
        pk=id
    )
    if (post_page.author.username != request.user.username
            and post_page.is_published is not True):
        raise Http404
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
    if username != request.user.username:
        post = user.posts(manager='published').all()
    else:
        post = (
            user.posts
            .prefetch_related('comments')
            .select_related('location', 'author', 'category')
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )
    page_obj = control_paginator(
        request.GET.get('page'),
        post
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
        return redirect(f'blog:profile', request.user.username)
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


@login_required
def profile_edit(request):
    template = 'blog/user.html'
    form = ProfileForm(request.POST or None, instance=request.user)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.username)
    return render(request, template, context)


@login_required
def edit_post(request, post_id):
    template = 'blog/create.html'
    post = get_object_or_404(
        Post.objects.select_related('location', 'author', 'category'),
        pk=post_id
    )
    if post.author.username != request.user.username:
        return redirect(f'blog:post_detail', post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    context = {'form': form}
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(f'blog:post_detail', post_id)
    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    template = 'blog/create.html'
    post = get_object_or_404(
        Post.objects.select_related('location', 'author', 'category'),
        pk=post_id
    )
    check_autor(post, request)
    context = {'form': PostForm(instance=post)}
    if request.method == 'POST':
        post.delete()
        return redirect(f'blog:profile', request.user.username)
    return render(request, template, context)


@login_required
def edit_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    comment = get_object_or_404(Comment, pk=comment_id)
    check_autor(comment, request)
    form = CommentForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = comment.post
        comment.save()
        return redirect('blog:post_detail', id=post_id)
    return render(request, template, context)


@login_required
def delete_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    comment = get_object_or_404(Comment, pk=comment_id)
    check_autor(comment, request)
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=post_id)
    return render(request, template, context)


def check_autor(db, request):
    if db.author.username != request.user.username:
        raise Http404


def get_post_user(post,user_boll):
    if user_boll:
        pass
    else:
        pass
