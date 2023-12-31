from typing import Any
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy, reverse
from .models import *
from django.db import connection, reset_queries
from django.views.generic import DetailView, DeleteView, UpdateView, ListView
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.conf import settings
from users.utils import check_group

from .utils import ViewCountMixin
from time import time

from .forms import *

#человек не аутентифицирован - отправляем на страницу другую

import json

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        return context

class ArticleUpdateView(ViewCountMixin, UpdateView):
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title','anouncement','text','tags']

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['image_form'] = ImagesFormSet(instance=current_object)
        return context

    def post(self, request, **kwargs):
        request.POST = request.POST
        current_object = Article.objects.get(id=request.POST['image_set-0-article'])
        deleted_ids = []
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])): #удаление всех по галочкам
            field_delete =f'image_set-{i}-DELETE'
            field_image_id = f'image_set-{i}-id'
            if field_delete in request.POST and request.POST[field_delete] =='on':
                image = Image.objects.get(id=request.POST[field_image_id])
                image.delete()
                deleted_ids.append(field_image_id)

                #тут же удалить картинку из request.FILES
        #Замена картинки
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_replace = f'image_set-{i}-image' #должен быть в request.FILES
            field_image_id = f'image_set-{i}-id'  #этот файл мы заменим
            if field_replace in request.FILES and request.POST[field_image_id] != '' and field_image_id not in deleted_ids:
                image = Image.objects.get(id=request.POST[field_image_id]) #
                image.delete() #удаляем старый файл
                for img in request.FILES.getlist(field_replace): #новый добавили
                    Image.objects.create(article=current_object, image=img, title=img.name)
                del request.FILES[field_replace] #удаляем использованный файл
        if request.FILES: #Добавление нового изображения
            print('!!!!!!!!!!!!!!!!!',request.FILES)
            for input_name in request.FILES:
                for img in request.FILES.getlist(input_name):
                    print('###############',img)
                    Image.objects.create(article=current_object, image=img, title=img.name)


        return super(ArticleUpdateView, self).post(request, **kwargs)

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news') #именованная ссылка или абсолютную
    template_name = 'news/delete_article.html'

class ArticleListView(ListView):
    model = Article
    template_name = 'news/news_list.html'

@login_required(login_url=settings.LOGIN_URL)
@check_group('Authors')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: #проверили что не аноним
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m()
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img, title=img.name)
                return redirect('news')
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

def search(request):
    if request.method == 'POST': #пришел запрос из бокового меню
        value = request.POST['search_input'] #находим новости
        articles = Article.objects.filter(title__icontains=value)
        if len(articles) == 1: #если одна- сразу открываем подробное отображение новости
            return render(request, 'news/news_detail.html', {'article': articles[0]})
        else:
            #если несколько - отправляем человека в функцию index со страницей-списком новостей и фильтрами
            #не забываем передать поисковый запрос:
            # либо через сессии:
            request.session['search_input'] = value
            return redirect('news')
            #либо через фрагмент URLссылки:
            # но в таком случае придётся обрабатывать ссылку в Urls
            #функция reverse из модуля Urls добавит переданные аргументы в качестве get-аргументов.
            # return redirect(reverse('news', kwargs={'search_input':value}))
            # return render(request, 'news/news_list.html', {'articles': articles})
    else:
        return redirect('main')


def news(request):
    all_articles_len = len(Article.objects.all()) # для цифры отфильтрованных новостей
    categories = Article.categories #создали перечень категорий
    author_list = User.objects.all() #создали перечень авторов
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        request.session['author_filter'] = selected_author
        request.session['category_filter'] = selected_category
        if selected_author == 0: #выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else: #если страница открывется впервые или нас переадресовала сюда функция поиск
        value = request.session.get('search_input') #вытаскиваем из сессии значение поиска
        if value != None: #если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(title__icontains=value)
            # del request.session['search_input'] #чистим сессию, чтобы этот фильтр не "заело"
        else: #если это не поисковый запрос, а переход по пагинатору или первое открытие
            selected_author = request.session.get('author_filter')
            selected_category = request.session.get('category_filter')
            articles = Article.objects.all()
            if selected_author != None and int(selected_author) != 0:  # если не пустое - находим нужные ноновсти
                articles = articles.filter(author=selected_author)
            else:
                selected_author = 0
            if selected_category != None and int(selected_category) != 0:  # фильтруем найденные по авторам результаты по категориям
                articles = articles.filter(category__icontains=categories[selected_category - 1][0])
            else:
                selected_category = 0

    #сортировка от свежих к старым новостям
    articles=articles.order_by('-date')
    total = len(articles)
    p = Paginator(articles,3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    # title = _('Заголовок страницы новости-индекс')
    context = {'articles': page_obj, 'author_list':author_list, 'selected_author':selected_author,
               'categories':categories,'selected_category': selected_category, 'total':total, 'all_articles_len': all_articles_len,
            #   'title':title
               }

    return render(request,'news/news_list.html',context)

#  старая пагинация
# def pagination(request):
#     articles = Article.objects.all()
#     p = Paginator(articles, 3)
#     page_number = request.GET.get('page')
#     page_obj = p.get_page(page_number)
#     print(page_obj)
#     context = {'articles': page_obj}
#     return render(request,'news/news_list.html',context)


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
