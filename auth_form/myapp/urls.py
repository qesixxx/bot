from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.user_list, name='user_list'),
    path("auth/", views.auth_page, name="auth_page")
]