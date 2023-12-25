from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count
from django.db import models
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user','gender']
    list_filter = ['user','gender']

from django.contrib.auth.models import Group
def make_author(modeladmin,request,queryset):
    group = Group.objects.get(name='Authors')
    ungroup = Group.objects.get(name='Pending Users')
    for user in queryset:
        user.groups.add(group)
        user.groups.remove(ungroup)

make_author.short_description = "Утвердить автора"

class CustomUserAdmin(UserAdmin):
    actions = [make_author]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ['article','user','create_at']
admin.site.register(FavoriteArticle, FavoriteArticleAdmin)

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
