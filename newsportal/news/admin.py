from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count

from .models import *

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date_change', 'author', 'title','date']
    list_display = ['title','author','date', 'date_change', 'symbols_count', 'slug']
    list_filter = ['title','author','date', 'date_change']
    list_display_links = ('date',)   #('title',) # - отображение поля как ссылки
    # list_editable = ['title'] # возможность редактирования из админки
    # readonly_fields = ['author']
    prepopulated_fields = {"slug":("title",)}
    list_per_page = 10 # отображение записей в админке

    @admin.display(description='Длина', ordering='_symbols')
    def symbols_count(self, article:Article):
        return f"Символы: {len(article.text)}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length('text'))
        return queryset

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','status','tag_count']
    list_filter = ['title','status']

    @admin.display(description='Частота использованяи тега:', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','article','image_tag']