from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Model
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from django.conf import settings
from .models import Post, Category, User, Comment
from .forms import CommentForm, PostForm, ProfileForm


class PaginateMixin:
    paginate_by = settings.ITEM_PER_PAGE


class DispatchBaseMixin:
    pk_url_kwarg: str
    model: Model
    post_id: str

    def dispatch(self, request, *args, **kwargs):
        query_set = get_object_or_404(self.model, pk=kwargs[self.pk_url_kwarg])
        if query_set.author != request.user:
            return redirect(
                'blog:post_detail',
                getattr(query_set, self.post_id)
            )
        return super().dispatch(request, *args, **kwargs)


class DispatchPostMixin(DispatchBaseMixin):
    pk_url_kwarg = 'post_id'
    model = Post
    post_id = 'id'


class DispatchCommentMixin(DispatchBaseMixin):
    pk_url_kwarg = 'comment_id'
    model = Comment
    post_id = 'post_id'


class IndexView(PaginateMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self) -> QuerySet:
        return Post.post_manager.published().all()


class CategoryView(PaginateMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet:
        category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        if not category.is_published:
            raise Http404
        return category.posts(manager='post_manager').published().all()


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None) -> Post:
        post = get_object_or_404(
            Post.post_manager.published(False),
            id=self.kwargs['id']
        )
        if (self.request.user != post.author
                and post.is_published is not True):
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': CommentForm(),
            'comments': self.object.comments.all()
        }


class ProfileListView(PaginateMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self, queryset=None) -> Post:
        user = get_object_or_404(User, username=self.kwargs['username'])
        is_author = self.request.user == user.username
        post = user.posts(manager='post_manager').published(is_author).all()
        self.user = user
        return post

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'profile': self.user
        }


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'includes/comments.html'
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'id': self.kwargs['post_id']})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post.post_manager.published(),
            id=self.kwargs['post_id']
        )
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user


class PostUpdateView(DispatchPostMixin, LoginRequiredMixin, UpdateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail', kwargs={'id': self.kwargs['post_id']})

    def form_valid(self, form):
        return super().form_valid(form)


class PostDeleteView(DispatchPostMixin, LoginRequiredMixin, DeleteView):
    template_name = 'blog/create.html'
    model = Post
    success_url = reverse_lazy('blog:profile')

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class CommentUpdateView(DispatchCommentMixin, LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'id': self.kwargs['post_id']})


class CommentDeleteView(DispatchCommentMixin, LoginRequiredMixin, DeleteView):
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'id': self.kwargs['post_id']})
