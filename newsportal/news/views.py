from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from .models import *
from django.db import connection, reset_queries
from django.views.generic import DetailView, DeleteView, UpdateView, ListView
from django.contrib.auth.decorators import login_required

from .forms import *
#человек не аутентифицирован - отправляем на страницу другую

import json

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title','anouncement','text','tags']

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news') #именованная ссылка или абсолютную
    template_name = 'news/delete_article.html'

class ArticleListView(ListView):
    model = Article
    template_name = 'news/news_list.html'

@login_required(login_url="/")
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: #проверили что не аноним
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m()
                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request,'news/create_article.html', {'form':form})

def search_news_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term','')
        articles = Article.objects.filter(title__icontains=q)
        results =[]
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)


def news(request):

    categories = Article.categories #создали перечень категорий
    author_list = User.objects.all() #создали перечень авторов
    all_articles_len = len(Article.objects.all()) # для цифры отфильтрованных новостей
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        if selected_author == 0: #выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else: #если страница открывется впервые
        selected_author = 0
        selected_category = 0
        articles = Article.objects.all()

    context = {'articles': articles, 'author_list':author_list, 'selected_author':selected_author,
               'categories':categories,'selected_category': selected_category, 'all_articles_len': all_articles_len}
    
    return render(request,'news/news_list.html',context)

def news_search(request):
    author_list = User.objects.all()
    selected = 0
    if request.method=="POST":
        selected = int(request.POST.get('author_filter'))
        if  selected == 0:
            articles = Article.objects.all()

# def detail(request, id):
#     article = Article.objects.filter(id=id)
#     return HttpResponse(f'<h1>{article}</h1>')
#     # return HttpResponse(f'<h1>{article.title}</h1>')

#     # articles = Article.objects.all()
#     # s=''
#     # for article in articles:
#     #     s+=f'<h1>{article.title}</h1><br>'
#     # return HttpResponse(s)
