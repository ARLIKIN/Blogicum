from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('create', views.create_post, name='create_post'),
    path('progile/edit', views.profile_edit, name='edit_profile'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('editpost/<int:post_id>', views.edit_post, name='edit_post'),
    path('deletepost/<int:post_id>', views.delete_post, name='delete_post'),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'),
    path(
            'deletecomment/<int:post_id>/<int:comment_id>',
            views.delete_comment,
            name='delete_comment')
]
