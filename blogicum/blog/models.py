from datetime import datetime

from django.db import models  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.urls import reverse  # type: ignore
from django.db.models import Count  # type: ignore

from core.models import PublishedAndCreatedModel
from blog.constants import MAX_CHAR_FIELD_LENGTH

User = get_user_model()


class Category(PublishedAndCreatedModel):
    title = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, цифры, дефис и'
                            ' подчёркивание.'
                            )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedAndCreatedModel):
    name = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,
                            verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedAndCreatedModel):
    title = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,
                             verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время в '
                                    'будущем — можно делать отложенные '
                                    'публикации.', null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        null=True
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    class SelectionManager(models.Manager):

        def selection(self):
            return self.select_related(
                'category', 'location', 'author'
            )

        def filtering_ordering(self):
            return self.selection().filter(
                is_published=True,
                category__is_published=True,
                pub_date__date__lte=datetime.now(),
            ).order_by(
                '-pub_date').annotate(
                comment_count=Count('comments'))

        def profile_ordering(self):
            return self.order_by(
                '-pub_date').annotate(
                comment_count=Count('comments'))

        def selection_for_category(self):
            return self.select_related(
                'category', 'location').filter(
                    is_published=True,
                    pub_date__date__lte=datetime.now())

        def filtered_by_category(self, category):
            return self.selection_for_category().filter(category=category)

    objects = models.Manager()
    selection = SelectionManager()


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
