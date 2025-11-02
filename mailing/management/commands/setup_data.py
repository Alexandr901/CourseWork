from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Наполнение базы данных начальными данными"

    def handle(self, *args, **options):
        # Создаем суперпользователя если его нет
        if not User.objects.filter(email="kokarev17@gmail.com").exists():
            User.objects.create_superuser(
                email="kokarev17@gmail.com", username="admin", password="admin123"
            )
            self.stdout.write(self.style.SUCCESS("Суперпользователь создан"))
        else:
            self.stdout.write(self.style.WARNING("Суперпользователь уже существует"))
