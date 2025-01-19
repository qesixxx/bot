from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_users(apps, schema_editor):
    UserProfile = apps.get_model('myapp', 'UserProfile')

    # Создаём пользователей
    UserProfile.objects.create(
        username='admin',
        password=make_password('12345678'),  # Хэшируем пароль
    )
    UserProfile.objects.create(
        username='user1',
        password=make_password('password1'),
    )
    UserProfile.objects.create(
        username='user2',
        password=make_password('password2'),
    )

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),  # Зависимость от предыдущей миграции
    ]

    operations = [
        migrations.RunPython(create_initial_users),
    ]