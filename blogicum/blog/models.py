import datetime as dt

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count

from core.models import PublishedModel, TitleModel


class Category(PublishedModel, TitleModel):
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, '
                  'дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


User = get_user_model()


class PostQuerySet(models.QuerySet):

    def published(self):
        return (
            self.with_related_data()
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=dt.datetime.now(tz=dt.timezone.utc)
            )
        )

    def with_related_data(self):
        return (
            self.prefetch_related('comments')
            .select_related('location', 'author', 'category')
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model).published()

    def with_related_data(self):
        return PostQuerySet(self.model).with_related_data()


class Post (PublishedModel, TitleModel):
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField('Фото', upload_to='blog_images', blank=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в '
                  'будущем — можно делать '
                  'отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='location',
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        verbose_name = 'публикация'
        default_related_name = 'posts'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(
        'Текст комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарий'
        default_related_name = 'comments'
        ordering = ('created_at',)

    def __str__(self):
        return self.text
