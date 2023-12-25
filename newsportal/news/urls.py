from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ArticleListView.as_view(), name = 'news'),   # использование viewslist
    # path('news/', views.ArticleListView.as_view(), name = 'news'),
    path('', views.news, name = 'news'),
    path('news/', views.news, name = 'news'),
    path('news/search_news_auto/', views.search_news_auto, name = 'search_news_auto'),
    path('news/<int:pk>', views.ArticleDetailView.as_view(), name = 'news_detail'),
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='news_delete'),
    path('create_article', views.create_article, name = 'create_article'),
    path('pagination', views.pagination, name = 'pagination'),
]
