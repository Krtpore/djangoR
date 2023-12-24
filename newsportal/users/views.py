from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

from .models import *
from .forms import *

def registration(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #появляется новый пользователь
            # group = Group.objects.get(name='Authors')
            # user.groups.add(group)

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


