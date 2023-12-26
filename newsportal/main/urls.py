from django.contrib import admin
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.main, name = 'main'),
    path('main/', views.main, name = 'main'),
    path('user/', views.user, name = 'user'),
    path('navbar/', views.navbar, name = 'navbar'),
    path('about/', views.about, name = 'about'),
    path('news_example/', views.news_example, name = 'news_example'),
    path('page404/', views.page404, name = 'page404'),
    path('update_server/', views.update_server, name='update_server'),
]

handler404 = 'main.views.page404'