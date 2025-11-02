from django.core.management.base import BaseCommand
from django.utils import timezone

from mailing.models import Mailing
from mailing.tasks import send_mailing


class Command(BaseCommand):
    help = "Запуск активных рассылок"

    def add_arguments(self, parser):
        parser.add_argument(
            "--mailing-id",
            type=int,
            help="ID конкретной рассылки для отправки",
        )

    def handle(self, *args, **options):
        mailing_id = options.get("mailing_id")

        if mailing_id:
            # Отправляем конкретную рассылку
            try:
                mailing = Mailing.objects.get(id=mailing_id)
                result = send_mailing.delay(mailing_id)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Запущена рассылка #{mailing_id}: {mailing.message.subject}"
                    )
                )
                self.stdout.write(f"Результат: {result.get(timeout=30)}")
            except Mailing.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Рассылка с ID {mailing_id} не найдена")
                )
        else:
            # Отправляем все активные рассылки
            now = timezone.now()
            active_mailings = Mailing.objects.filter(
                status="started", start_time__lte=now, end_time__gte=now
            )

            if not active_mailings:
                self.stdout.write(
                    self.style.WARNING("Нет активных рассылок для отправки")
                )
                return

            for mailing in active_mailings:
                send_mailing.delay(mailing.id)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Запущена рассылка #{mailing.id}: {mailing.message.subject}"
                    )
                )
