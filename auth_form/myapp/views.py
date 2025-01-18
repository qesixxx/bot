from django.contrib.auth import authenticate, login as user_login
from django.http import HttpResponseRedirect
from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')  # Используем переменную username для логина
        password = request.POST.get('password')  # Получаем пароль из POST-запроса

        usr = authenticate(request, username=username, password=password)
        if usr is not None:
            user_login(request, usr)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'myapp/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'myapp/login.html')