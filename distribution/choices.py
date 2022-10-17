from django.db.models import TextChoices


class MessageStatus(TextChoices):
    """Статусы сушности сообщения."""

    pending = 'pending', 'в ожидании отправления'
    not_send = 'not_sent', 'не отправленно'
    sent = 'sent', 'отправленно'
    canceled = 'canceled', 'отменено'
