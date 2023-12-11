from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name = 'news'),
    path('news/', views.news, name = 'news'),
    path('news/<int:id>', views.detail, name = 'news_detail'),
]
