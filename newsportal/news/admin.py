from django.contrib import admin

from .models import *

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date_change', 'author', 'title','date']
    list_display = ['title','author','date', 'date_change']
    list_filter = ['title','author','date', 'date_change']
    list_display_links = ('date',)   #('title',) # - отображение поля как ссылки
    list_editable = ['title'] # возможность редактирования из админки
    readonly_fields = ['author']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['title','status']

# admin.site.register(Tag,TagAdmin) - заменили на декоратор
# admin.site.register(Article,ArticleAdmin)