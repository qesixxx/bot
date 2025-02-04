# myapp/views.py
from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth.decorators import login_required  # Добавлено
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile  # исправлено
import logging  # Для отладки вместо print
from django.contrib import messages

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)
            return redirect(reverse('auth_page'))
        else:
            return render(request, 'myapp/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'myapp/login.html')

def index_view(request):
    return render(request, 'myapp/index.html')

def user_list(request):
    users = UserProfile.objects.all()
    logger.info(f"Список пользователей: {users}")  # Заменил print на logger
    return render(request, 'myapp/user_list.html', {'users': users})

@login_required(login_url='/login/')  # Перенаправление на страницу входа
def auth_page(request):
    return render(request, "myapp/auth.html")
