# auth_form/urls.py
from django.contrib import admin
from django.urls import path, include
from myapp import views  # исправлено

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут для админки
    path('users/', include('myapp.urls')),  # Маршрут для списка пользователей
    path('login/', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
]