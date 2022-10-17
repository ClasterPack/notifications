import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from distribution.choices import MessageStatus


class Client(models.Model):
    """Модель Клиента."""

    timezones = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    id = models.AutoField(primary_key=True, auto_created=True)
    phone_regex = RegexValidator(
        regex=r'^7\d{10}$',
        message='Неверный номер телефона клиента,введите номер в формате:'
                ' 7XXXXXXXXXX (X - number from 0 to 9)',
    )
    phone_number = models.CharField(
        _('номер телефона'),
        validators=[phone_regex],
        unique=True,
        max_length=11,
    )
    operator_code = models.CharField(_('код мобильного оператора'), max_length=3)
    tag = models.TextField(_('тег'), blank=True)
    timezone = models.CharField(
        _('часовой пояс'),
        max_length=32,
        choices=timezones,
        default='UTC',
    )

    def __str__(self):
        """Название в бд по номеру телефона."""
        return str(self.phone_number)

    class Meta:
        """Переименовываем модель в бд."""

        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Messages(models.Model):
    """Модель сущности сообшений."""

    id = models.AutoField(primary_key=True, auto_created=True)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(
        _('статус сообщения'),
        choices=MessageStatus.choices,
        default='pending',
        max_length=9,
    )
    client_id = models.IntegerField(_('id клиента'))
    distribution_id = models.IntegerField(_('id Рассылки'))

    class Meta:
        """Переименовываем модель в бд."""

        verbose_name = 'сущность сообщения'
        verbose_name_plural = 'сущность сообщения'


class Distribution(models.Model):
    """Класс Рассылок."""

    id = models.AutoField(primary_key=True, auto_created=True)
    start_time = models.DateTimeField(_('время начала рассылки'))
    filter_tag = models.TextField(_('фильтр по тегу'), blank=True)
    filter_operator_code = models.CharField(
        _('фильтр по коду оператора'),
        max_length=3,
        blank=True,
    )
    end_time = models.DateTimeField(_('окончание рассылки'))
    message = models.TextField(_('сообщение'))

    @property
    def to_send(self):
        """Проверка на необходимость отправки."""
        now = timezone.now()
        if self.start_time <= now <= self.end_time:
            return True
        else:
            return False

    @property
    def delay_sent(self):
        """Проверка на необходимость задержки при отправки."""
        now = timezone.now()
        if self.start_time > now <= self.end_time:
            return True
        else:
            return False

    class Meta:
        """Переименовываем модель класса в бд."""

        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
