from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name = 'news_index'),
    # path('news/', views.news, name = 'news_list'),
]

