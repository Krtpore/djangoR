from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from news.models import Article

from .forms import AccountUpdateForm, UserUpdateForm
from django.core.paginator import Paginator

# from django.core.mail import send_mail  - рассылк почты

from .models import *
from .forms import *
from .utils import *


def profile(request):
    context = dict()
    return render(request,'users/profile.html',context)

@login_required
def add_to_favorites(request, id):
    article = Article.objects.get(id=id)
    #проверям есть ли такая закладка с этой новостью
    bookmark = FavoriteArticle.objects.filter(user=request.user.id,
                                              article=article)
    if bookmark.exists():
        bookmark.delete()
        messages.warning(request,f"Новость {article.title} удалена из закладок")
    else:
        bookmark = FavoriteArticle.objects.create(user=request.user, article=article)
        messages.success(request,f"Новость {article.title} добавлена в закладки")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def profile_update(request):
    user = request.user
    account = Account.objects.get(user=user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request,"Профиль успешно обновлен")
            return redirect('profile')
        else:
            pass
    else:
        context = {'account_form':AccountUpdateForm(instance=account),
                   'user_form':UserUpdateForm(instance=user)}
    return render(request,'users/edit_profile.html',context)

def password_update(request):
    user = request.user
    form = PasswordChangeForm(user,request.POST)
    if request.method == 'POST':
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request,password_info)
            messages.success(request,'Пароль успешно изменен')
            return redirect('profile')

    context = {"form": form}
    return render(request,'users/edit_password.html',context)

def registration(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #появляется новый пользователь
            category = request.POST['account_type']
            if category == 'author':
                group = Group.objects.get(name='Pending Users')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Reader')
                user.groups.add(group)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = Account.objects.create(user=user,nickname=user.username)

            authenticate(username=username,password=password)
            messages.success(request,f'{username} был зарегистрирован!')
            login(request,user)
            return redirect ('first_redirect') # ('main') ошибка 500 после регистрации, сделал редирект на 1ый вход
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'users/registration.html', context)

@login_required
def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print('Сообщение отправлено', form.cleaned_data)
        else:
            print(form.errors)
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request,'users/contact_page.html',context)

@login_required
def profile_delete(request):
    user = request.user
    user.delete()
    return redirect('main')

def index(request):
    print(request.user, request.user.id)
    user_acc = Account.objects.get(user=request.user)
    print(user_acc)
    return HttpResponse('Приложениt Users')

def my_news_list(request):
    categories = Article.categories #создали перечень категорий
    author = User.objects.get(id=request.user.id) #создали перечень авторов
    articles = Article.objects.filter(author = author)
    if request.method == "POST":
        selected_category = int(request.POST.get('category_filter'))
        if selected_category != 0: #фильтруем найденные результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else: #если страница открывется впервые
        selected_category = 0
        # articles = Article.objects.all()

    total = len(articles)

    p = Paginator(articles,3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'total':total,
               'categories':categories,'selected_category': selected_category}

    return render(request,'users/my_news_list.html',context)



def my_favorites(request):
    categories = Article.categories
    author_list = User.objects.all()
    favlist=FavoriteArticle.objects.filter(user=request.user.id)
    articles = Article.objects.filter(favoritearticle__in=favlist)
    total = len(articles)
    p = Paginator(articles,3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    selected_author = 0
    selected_category = 0
    context = {'articles': page_obj,
               'author_list':author_list,
               'selected_author':selected_author,
               'categories':categories,
               'selected_category': selected_category,
               'total':total,}

    return render(request,'users/my_favorites.html',context)
