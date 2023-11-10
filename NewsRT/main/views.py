from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import News, Product

def index(request):
    # value = -10
    # n1 = News('Новость 1', 'текст 1', 'Дата 1')
    # n2 = News('Новость 2', 'текст 2', 'Дата 2')
    # m = [n1, n2]
    # l = ['раз', 'два', 'три']
    # context = {'title':'Страница главная',
    #            'Header1':'Заголовок страницы',
    #            'value': value,
    #            'numbers': l,
    #            'news': m}




    colors = ['red', 'blue', 'golden', 'black']
    context = {
        'colors':colors,
        # 'water': water,
        # 'chocolate': chocolate,
    }
    if request.method == "POST":
        print(request.POST)
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product(title,float(price),int(quantity))
        print('Создан товар:',new_product.title, 'Общая сумма:',new_product.amount)
    else:
        print(request.GET)

    return render(request, 'main/index.html', context)

def get_demo(request, a):
    return HttpResponse(f'Вы ввели: {a}')

def get_calc(request, a, operation, b):
    # match operation:
    #     case 
    if operation == "multiply":
        return HttpResponse(f'Вы ввели: {a}, {operation}, {b} Результат {a * b}')
    elif operation == "divide":
        return HttpResponse(f'Вы ввели: {a}, {operation}, {b} Результат {a / b}')
    elif operation == "plus":
        return HttpResponse(f'Вы ввели: {a}, {operation}, {b} Результат {a + b}')
    elif operation == "minus":
        return HttpResponse(f'Вы ввели: {a}, {operation}, {b} Результат {a - b}')
    elif operation == "power":
        return HttpResponse(f'Вы ввели: {a}, {operation}, {b} Результат {a ** b}')
    else:
        return HttpResponse(f'Неверная команда')

def about(request):
    return HttpResponse('<h1> Тут про нас </h1>')

def contacts(request):
    return HttpResponse('<h1> Тут наши контакты </h1>')

def sidebar(request):
    return render(request, 'main/sidebar.html')

def custom_404(request, exception):
    #return render(request, '')
    return HttpResponse(f'Оуоуоу, полегче, ошибка: {exception}')