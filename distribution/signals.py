from celery.beat import logger
from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from distribution.models import (Client, Distribution, DistributionTasks,
                                 Messages)
from distribution.tasks import send_notification
from notifications.celery import app


@receiver(post_save, sender=Distribution, dispatch_uid='create_notification')
def create_notification(sender, instance, created, update_fields, **kwargs):
    """Создаем сушность сообщений, и создаем таску."""
    if created:
        distribution = Distribution.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(
            Q(operator_code=distribution.filter_operator_code) |
            Q(tag=distribution.filter_tag),
        ).all()
        for client in clients:
            Messages.objects.create(
                status='pending',
                client_id=client.id,
                distribution_id=distribution.id,
            )
            message = Messages.objects.filter(distribution_id=distribution.id, client_id=client.id).first()
            data = {
                'id': message.id,
                'phone': client.phone_number,
                'text': distribution.message,
            }
            client_id = client.id
            distribution_id = distribution.id

            if instance.to_send:
                send_notification.apply_async(
                    (data, client_id, distribution_id),
                    expires=distribution.end_time,
                )

            elif instance.delay_sent:
                send_notification.apply_async(
                    (data, client_id, distribution_id),
                    eta=distribution.start_time,
                    expires=distribution.end_time,
                )

            else:
                send_notification.apply_async(
                    (data, client_id, distribution_id),
                    eta=distribution.start_time,
                    expires=distribution.end_time,
                )
                message = Messages.objects.filter(
                    distribution_id=distribution_id,
                    client_id=client_id,
                ).first()
                message.status = 'not_sent'
                message.save()


@receiver(post_delete, sender=Distribution, dispatch_uid='delete_notification')
def delete_notification(sender, instance, **kwargs):
    """Удаление очереди сообщений при удалении модели Distribution(Оповешений)."""
    distribution = Distribution.objects.filter(id=instance.id).first()
    tasks = DistributionTasks.objects.filter(distribution=distribution).all()
    Messages.objects.filter(
        distribution_id=instance.id,
        status='pending',
    ).all().update(
        status='canceled',
    )
    for task in tasks:
        try:
            app.control.revoke(task.task_id, terminate=True)

        except Exception as exc:
            logger.exception(exc)
