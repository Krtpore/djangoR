from django.contrib import admin
from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<int:a>/details', views.get_demo),
    path('product/<int:a>/<slug:operation>/<int:b>', views.get_calc),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('sidebar/', views.sidebar),
]