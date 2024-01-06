from django.contrib import admin
from django.urls import path

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import main.views as main_views

from . import views
from .views import *

urlpatterns = [
    path('', views.main, name = 'main'),
    path('main/', views.main, name = 'main'),
    path('navbar/', views.navbar, name = 'navbar'),
    path('about/', views.about, name = 'about'),
    path('news_example/', views.news_example, name = 'news_example'),
    path('page404/', views.page404, name = 'page404'),
    # path('update_server/', main_views.update_server, name='update_server'),  # закомментировано до рассылки видеоурока
]

handler404 = 'main.views.page404'