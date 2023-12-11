from django.shortcuts import render, HttpResponse

from .models import *

def news(request):
    articles = Article.objects.all()
    context = {'articles':articles}
    return render(request, 'news/news.html', context)

def news_search(request):
    author_list = User.objects.all()
    selected = 0
    if request.method=="POST":
        selected = int(request.POST.get('author_filter'))
        if  selected == 0:
            articles = Article.objects.all()

    #     else:
    #         articles = Article.objects.filter(author=selected)
    # else:
    #     articles = Article.objects.all()
    # context = {'articles':articles, 'author_list':author_list,'selected':selected }
    # return render(request,'news/news_list.html',context)
    
    # для справки
    # articles = Article.objects.all().first()
    # print(articles)
    # articles = Article.objects.filter(author=request.user.id)
    # print('автор новости', article.title, ':', article.author.username)
    # print(articles)
    # articles = Article.objects.get(author=2)
    
    # tag = Tag.objects.filter(title='World')[0]
    # tagged_news = Article.objects.filter(tags=tag)
    # print(tagged_news)

    # user_list = User.objects.all()
    # print(user_list)
    # for user in user_list:
    #     print(user, Article.objects.filter(author=user))

def detail(request, id):
    article = Article.objects.filter(id=id)
    return HttpResponse(f'<h1>{article}</h1>')
    # return HttpResponse(f'<h1>{article.title}</h1>')

    # articles = Article.objects.all()
    # s=''
    # for article in articles:
    #     s+=f'<h1>{article.title}</h1><br>'
    # return HttpResponse(s)
