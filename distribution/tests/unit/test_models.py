import datetime

from data_for_tests import good_clinets_data
from django.test import TestCase
from freezegun import freeze_time

from distribution.models import Client, Distribution, Messages


class TestModel(TestCase):
    """Тестирование моделей."""

    def setUp(self):
        """Настройка для тестирования модели."""
        self.freezer = freeze_time('2022-10-14 12:00:00')
        self.freezer.start()
        self.clients = good_clinets_data

    def test_create_distribution_and_time_freezer(self):
        """Тест создания модели уведомлений."""
        distribution = Distribution.objects.create(
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(days=1),
            filter_tag='test',
            filter_operator_code=999,
            message='test message',
        )
        self.assertIsInstance(distribution, Distribution)
        self.assertEqual(distribution.start_time, datetime.datetime(2022, 10, 14, 12, 0))
        self.assertEqual(distribution.filter_operator_code, 999)
        self.assertEqual(distribution.filter_tag, 'test')

    def test_clint_creation(self):
        """Тесто создания модели Клиента."""
        client = Client.objects.create(
            phone_number=79994998877,
            operator_code=999,
            tag='vasya',
            timezone='UTC',
        )
        self.assertIsInstance(client, Client)
        self.assertEqual(client.tag, 'vasya')
        self.assertEqual(client.timezone, 'UTC')
        self.assertEqual(client.phone_number, 79994998877)

    def test_messages_creation(self):
        """Тест создания модели сообщений."""
        messages = Messages.objects.create(
            status='pending',
            client_id=1,
            distribution_id=1,
        )
        self.assertIsInstance(messages, Messages)
        self.assertEqual(messages.status, 'pending')
        self.assertEqual(messages.client_id, 1)
        self.assertEqual(messages.distribution_id, 1)
