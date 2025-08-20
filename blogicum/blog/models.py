from django.contrib.auth.models import User
from django.db import models
from django import forms

from blog.constants import MAX_TEXT_SIZE
from blog.managers import FilterPostManager
from blog.querysets import PostQuerySet


class PublishAndCreateModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(PublishAndCreateModel):
    title = models.CharField(
        max_length=MAX_TEXT_SIZE,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены '
                  'символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishAndCreateModel):
    name = models.CharField(
        max_length=MAX_TEXT_SIZE,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(PublishAndCreateModel):
    title = models.CharField(
        max_length=MAX_TEXT_SIZE,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='post_category'
    )
    image = models.ImageField(
        upload_to='posts_image',
        blank=True,
        verbose_name='Фото'
    )

    objects = PostQuerySet.as_manager()
    filter_manager = FilterPostManager()

    def comments_count(self):
        return self.comments.count()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',) 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
