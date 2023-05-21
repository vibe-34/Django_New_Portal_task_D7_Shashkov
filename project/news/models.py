from django.contrib.auth.models import User
from django.db import models


class Record(models.Model):  # Класс публикации
    title = models.CharField('Название', max_length=64)
    full_text = models.TextField('Статья')
    data = models.DateTimeField('Дата публикации')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def preview(self):
        preview = f'{self.full_text[:128]}...'
        return preview

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:                       # Класс для переименования таблицы в админке. Обязательное название класса - Meta
        verbose_name = 'Новость'         # Указываем название таблицы в единственном числе
        verbose_name_plural = 'Новости'  # Указываем название таблицы во множественном числе


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
