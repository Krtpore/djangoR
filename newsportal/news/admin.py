from typing import Any
from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count
from django.db.models.query import QuerySet

from .models import *

class ArticleFilter(admin.SimpleListFilter):
    title = 'По длине новости'
    parameter_name = 'text'
    
    def lookups(self, request, model_admin):
        return [('S',("Короткие, <100 зн.")),
                ('M',("Средние, 100-500 зн.")),
                ('L',("Длинные, >500 зн.")),]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=500,
                                                                     text_len__gte=100,)
        elif self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=500)

class ArticleImageInLine(admin.TabularInline):
    model = Image
    extra = 3
    readonly_fields = ('id', 'image_tag')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date_change', 'author', 'title','date']
    list_display = ['title','author', 'status', 'date', 'date_change', 'symbols_count', 'slug', 'image_tag']
    list_filter = ['author','date', 'date_change', ArticleFilter]
    list_display_links = ('title', 'date',)   #('title',) # - отображение поля как ссылки
    list_editable = ['status'] # возможность редактирования из админки
    search_fields = ['title', 'tags__title']
    filter_horizontal = ['tags'] #filter_vertical = ['tags'] # разное отображение
    # readonly_fields = ['author']
    prepopulated_fields = {"slug":("title",)}
    actions = ['set_true', 'set_false']
    list_per_page = 15 # отображение записей в админке
    inlines = [ArticleImageInLine,]

    @admin.display(description='Длина', ordering='_symbols')
    def symbols_count(self, article:Article):
        return f"Символы: {len(article.text)}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length('text'))
        return queryset
        
    @admin.action(description="Опубликовать новости")
    def set_true(self,request,queryset):
        amount = queryset.update(status=True)
        self.message_user(request, f'Опубликовано {amount} новостей')

    @admin.action(description="Снять с публикации")
    def set_false(self,request,queryset):
        amount = queryset.update(status=False)
        self.message_user(request, f'Сняты с публикации {amount} шт.')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','status','tag_count']
    list_filter = ['title','status']
    actions = ['set_true', 'set_false']

    @admin.display(description='Частота использованяи тега:', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset
    
    @admin.action(description="Активировать теги")
    def set_true(self,request,queryset):
        amount = queryset.update(status=True)
        self.message_user(request, f'Активировано {amount} тегов')

    @admin.action(description="Деактивировать теги")
    def set_false(self,request,queryset):
        amount = queryset.update(status=False)
        self.message_user(request, f'Деактивировано {amount} тегов')
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','article','image_tag']