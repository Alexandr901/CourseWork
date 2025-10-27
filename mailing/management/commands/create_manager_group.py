from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from mailing.models import Client, Mailing, Message
from users.models import User


class Command(BaseCommand):
    help = "Создание группы менеджеров и назначение прав"

    def handle(self, *args, **options):
        # Создаем или получаем группу менеджеров
        manager_group, created = Group.objects.get_or_create(name="Менеджеры")

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует'))

        # Получаем необходимые права
        permissions = []

        # Права для модели Mailing
        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        permissions.extend(
            Permission.objects.filter(
                content_type=mailing_content_type,
                codename__in=["view_all_mailings", "disable_mailing"],
            )
        )

        # Права для модели Message
        message_content_type = ContentType.objects.get_for_model(Message)
        permissions.extend(
            Permission.objects.filter(
                content_type=message_content_type, codename="view_all_messages"
            )
        )

        # Права для модели Client
        client_content_type = ContentType.objects.get_for_model(Client)
        permissions.extend(
            Permission.objects.filter(
                content_type=client_content_type, codename="view_all_clients"
            )
        )

        # Права для модели User
        user_content_type = ContentType.objects.get_for_model(User)
        permissions.extend(
            Permission.objects.filter(
                content_type=user_content_type,
                codename__in=["view_user", "change_user", "delete_user"],
            )
        )

        # Назначаем права группе
        manager_group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(f'Назначено {len(permissions)} прав группе "Менеджеры"')
        )

        # Выводим список назначенных прав
        self.stdout.write("Назначенные права:")
        for perm in permissions:
            self.stdout.write(f"  - {perm.name}")
