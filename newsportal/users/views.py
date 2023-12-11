from django.shortcuts import render, HttpResponse

from .models import *

# Create your views here.
def index(request):
    print(request.user, request.user.id)
    user_acc = Account.objects.get(user=request.user)
    print(user_acc)
    return HttpResponse('Приложениt Users')


