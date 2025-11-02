import logging

# Получаем логгер для приложения рассылок
logger = logging.getLogger("mailing")


def log_mailing_creation(mailing, user):
    """Логирование создания рассылки"""
    logger.info(
        f"Создана рассылка #{mailing.id} '{mailing.title}' пользователем {user.email}"
    )


def log_mailing_sent(mailing, success=True, recipients=0, error=None):
    """Логирование отправки рассылки"""
    status = "успешно" if success else "с ошибкой"
    message = f"Рассылка #{mailing.id} отправлена {status}. Получателей: {recipients}"
    if error:
        message += f". Ошибка: {error}"

    if success:
        logger.info(message)
    else:
        logger.error(message)


def log_mailing_error(mailing, error):
    """Логирование ошибки в рассылке"""
    logger.error(f"Ошибка в рассылке #{mailing.id}: {error}")


def log_user_action(user, action, target=None):
    """Логирование действий пользователя"""
    message = f"Пользователь {user.email} выполнил действие: {action}"
    if target:
        message += f" -> {target}"
    logger.info(message)
