from django.contrib import admin
from django.urls import path, include
from auth_form.myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут для админки
    path('users/', include('myapp.urls')),  # Маршрут для списка пользователей
    path('', views.login_view, name='login'),  # Маршрут для корневого пути (авторизация)
]
