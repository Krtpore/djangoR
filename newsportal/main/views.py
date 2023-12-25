from django.shortcuts import render

from django.views import defaults

def page404(request, exception):
    return render(request, 'main/page404.html')

def main(request):
    return render(request, 'main/main.html')

def news(request):
    return render(request, 'main/news.html')

def user(request):
    return render(request, 'main/user.html')

def navbar(request):
    return render(request, 'main/navbar.html')

def about(request):
    return render(request, 'main/about.html')

def base(request):
    return render(request, 'main/base.html')

def news_example(request):
    return render(request, 'main/news_example.html')

def user(request):
    return render(request, 'main/user.html')
