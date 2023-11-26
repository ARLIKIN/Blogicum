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
    path('comment/<int:post_id>', views.add_comment, name='add_comment')
]
