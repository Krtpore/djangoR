from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name = 'news'),
    path('news/', views.news, name = 'news'),
    path('news/search_news_auto/', views.search_news_auto, name = 'search_news_auto'),
    path('news/<int:id>', views.detail, name = 'news_detail'),
    path('create_article', views.create_article, name = 'create_article'),
]
