from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    # Указываем, какое поле используется как уникальный идентификатор
    USERNAME_FIELD = 'username'

    # Указываем, что нет обязательных полей, кроме username и password
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username