from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from .forms import AccountUpdateForm, UserUpdateForm

from .models import *
from .forms import *

def profile(request):
    context = dict()
    return render(request,'users/profile.html',context)


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
            group = Group.objects.get(name='Authors')
            user.groups.add(group)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            #!!!не аутентифицируется - нужно доделать
            authenticate(username=username,password=password)
            messages.success(request,f'{username} был зарегистрирован!')
            return redirect('main')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'users/registration.html', context) 

    # if request.method=='POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save() #появляется новый пользователь
    #         category = request.POST['account_type']
    #         if category == 'author':
    #             group = Group.objects.get(name='Actions Required')
    #             user.groups.add(group)
    #         else:
    #             group = Group.objects.get(name='Reader')
    #             user.groups.add(group)
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password1')
    #         account = Account.objects.create(user=user,nickname=user.username)
    #         user = authenticate(username=username,password=password)
    #         login(request,user)
    #         messages.success(request,f'{username} был зарегистрирован!')

    #         return redirect('home')
    # else:
    #     form = UserCreationForm()
    # context = {'form':form}
    # return render(request,'users/registration.html',context)


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Сообщение отправлено', form.cleaned_data)
        else:
            print(form.errors)
    else:
        form = ContactForm()
        form.name='Любимый клиент'
    context = {'form': form}
    return render(request,'users/contact_page.html',context)


def index(request):
    print(request.user, request.user.id)
    user_acc = Account.objects.get(user=request.user)
    print(user_acc)
    return HttpResponse('Приложениt Users')


