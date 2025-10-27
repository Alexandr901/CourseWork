from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Client, Mailing, MailingAttempt


@shared_task
def send_mailing(mailing_id):
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        clients = mailing.clients.all()

        # Обновляем статус рассылки
        if mailing.status != "started":
            mailing.status = "started"
            mailing.save()

        successful_sends = 0
        failed_sends = 0

        for client in clients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=None,  # Используется DEFAULT_FROM_EMAIL
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="success",
                    server_response="Успешно отправлено",
                    client=client,
                )
                successful_sends += 1

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="failure",
                    server_response=str(e),
                    client=client,
                )
                failed_sends += 1

        # Проверяем, не закончилось ли время рассылки
        if mailing.end_time <= timezone.now():
            mailing.status = "completed"
            mailing.save()

        return {
            "mailing_id": mailing_id,
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "total_sends": successful_sends + failed_sends,
        }

    except Mailing.DoesNotExist:
        return {"error": f"Рассылка с ID {mailing_id} не найдена"}
