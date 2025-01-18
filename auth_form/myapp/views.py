from django.contrib.auth import authenticate, login as user_login
from django.http import HttpResponseRedirect
from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            return render(request, 'myapp/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'myapp/login.html')

def index_view(request):
    return render(request, 'myapp/index.html')