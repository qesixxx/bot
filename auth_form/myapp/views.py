from django.contrib.auth import authenticate, login as user_login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render
from .models import UserProfile  # Импорт модели UserProfile

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



def user_list(request):
    users = UserProfile.objects.all()  # Получаем всех пользователей
    return render(request, 'myapp/user_list.html', {'users': users})