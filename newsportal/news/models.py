from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

import datetime

class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday,self).get_queryset().filter(date__gte=datetime.date.today())

class Article(models.Model):
    categories = (('E', 'Экономика'),
                  ('S', 'Наука'),
                  ('IT', 'IT'),
                  ('SP', 'Спорт'),
                  ('N', 'Природа'),
                  ('W', 'Мировые новости'),
                  ('R', 'Региональные новости'),
                  ('C', 'Культура'),
                  ('R', 'Региональные новости'))
    # поля новости
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    title = models.CharField('Название', max_length=120, default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_now_add=True)
    date_change = models.DateTimeField('Дата обновления', auto_now = True)
    category = models.CharField(choices=categories, max_length=20, verbose_name='Категория')
    tags = models.ManyToManyField(to=Tag, blank=True)
    slug = models.SlugField()
    objects = models.Manager()
    published = PublishedToday()

    def __str__(self):
        return f'Новость: {self.title} опубликована: {str(self.date)[:16]}, последнее изменение: {str(self.date_change)[:16]}'
    
    def get_absolute_url(self):
        return f'/news/news/{self.id}'
    
    def tag_list(self):
        s = ''
        for t in self.tags.all():
            s+=t.title+' '
        return s

    class Meta:
        ordering = ['title','date']
        verbose_name= 'Новость'
        verbose_name_plural='Новости'

class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='article_images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.image.url}" height="40px" width="auto" />')
        else:
            return '(no image)'
        
    class Meta:
        # ordering = ['title','date']
        verbose_name= 'Картинка новости'
        verbose_name_plural='Картинки новостей'

