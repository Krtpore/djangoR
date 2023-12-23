from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count
from django.db import models

from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user','gender']
    list_filter = ['user','gender']

# мое
# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ['title','article','image_tag']

# class AccountAdmin(admin.ModelAdmin):
#     list_display = ['user','gender']
#     list_filter = ['user','gender']

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
    # list_display = ['user','gender', 'email', 'birthdate', 'email', 'account_image', 'user_count']
    # list_filter = ['user','gender', 'email', 'birthdate', 'email', 'account_image']

    # @admin.display(description='Новостей у пользователя:', ordering='user_count')
    # def user_count(self, object):
    #     return object.user_count

    # def get_queryset(Article, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(user_count=Count('article'))
    #     return queryset


admin.site.register(Account,AccountAdmin)
