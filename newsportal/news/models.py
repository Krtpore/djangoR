from django.db import models

from django.contrib.auth.models import User


class Article(models.Model):
    # поля новости
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название', max_length=50, default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_created = True)
    date_change = models.DateTimeField('Дата обновления', auto_now = True)