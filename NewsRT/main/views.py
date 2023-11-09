from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import News

def index(request):
    value = -10
    n1 = News('Новость 1', 'текст 1', 'Дата 1')
    n2 = News('Новость 2', 'текст 2', 'Дата 2')
    m = [n1, n2]
    l = ['раз', 'два', 'три']
    context = {'title':'Страница главная',
               'Header1':'Заголовок страницы',
               'value': value,
               'numbers': l,
               'news': m}
    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('<h1> Тут про нас </h1>')

def contacts(request):
    return HttpResponse('<h1> Тут наши контакты </h1>')

def sidebar(request):
    return render(request, 'main/sidebar.html')