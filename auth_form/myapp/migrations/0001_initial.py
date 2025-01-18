from django.db import migrations
from django.contrib.auth.models import User

def create_users(apps, schema_editor):
    User.objects.create_user(username='admin', password='12345678')

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),  # Зависимость от предыдущей миграции
    ]

    operations = [
        migrations.RunPython(create_users),
    ]