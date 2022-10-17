import datetime
import os

import pytz
import requests
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

from distribution.models import Client, Distribution, Messages
from notifications.celery import app

logger = get_task_logger(__name__)

load_dotenv()
URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')


@app.task(bind=True, retry_backoff=True)
def send_notification(self, data, client_id, distribution_id, url=URL, token=TOKEN):
    """Функция для создания таски. Таски выполняет запросы во внешнее API."""
    notification = Distribution.objects.get(id=distribution_id)
    client = Client.objects.get(id=client_id)
    timezone = pytz.timezone(client.timezone)
    now = datetime.datetime.now(timezone)
    if notification.start_time <= now <= notification.end_time:
        header = {
            'Authorisation': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        try:
            requests.post(
                url=url + (data['id']),
                headers=header,
                json=data,
            )
        except requests.exceptions.RequestException as exception:
            logger.error(f"id сообщения:{data['id']} , ошибка отправки.")
            Messages.objects.filter(id=data['id'].update(status='not_sent'))
            raise self.retry(exc=exception)
        else:
            logger.info(f"message id:{data['id']}, Статус сообщения: отпправленно")
            Messages.objects.filter(id=data['id']).update(status='sent')
    else:
        logger.error(f"id сообщения:{data['id']} , не подходящее время для отправки сообщения.")
        Messages.objects.filter(id=data['id'].update(status='not_sent'))
        return self.retry(coountdown=60 * 60)
