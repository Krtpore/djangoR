from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('main/', views.main, name = 'main'),
    path('user/', views.user, name = 'user'),
    path('navbar/', views.navbar, name = 'navbar'),
    path('page404/', views.page404, name = 'page404'),
    path('about/', views.about, name = 'about'),
    path('news_example/', views.news_example, name = 'news_example'),
]

