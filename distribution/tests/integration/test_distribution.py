from django.test import Client, TestCase


class TestDistribution(TestCase):
    """Тест кейс для рассылки."""

    def setUp(self):
        """Настройка данных класса и создание клиента для проверки реквестов."""
        self.client = Client()
        self.good_data = {
            'start_time': '2026-12-31T21:27:00Z',
            'filter_tag': 'tests',
            'filter_operator_code': '999',
            'end_time': '2099-10-10T21:28:00Z',
            'message': 'tests',
        }
        self.good_data_check = {
            'id': 1,
            'start_time': '2026-12-31T21:27:00Z',
            'filter_tag': 'tests',
            'filter_operator_code': '999',
            'end_time': '2099-10-10T21:28:00Z',
            'message': 'tests',
        }
        self.bad_data = {
            'tests': 'tests',
        }

    def test_get_response(self):
        """Тест на чтение данных(get request)."""
        response = self.client.get('/distribution/')
        self.assertEqual(response.status_code, 200)

    def test_post_response(self):
        """Тест на добавления данных(post request)."""
        response = self.client.post('/distribution/?format=json', self.good_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, self.good_data_check)

    def test_delete_request(self):
        """Тест на удаление данных(delete request)."""
        self.client.post('/distribution/?format=json', self.good_data)
        response = self.client.delete('/distribution/1/')
        self.assertEqual(response.status_code, 204)

    def test_non_updatable_data(self):
        """Test non-updatable data(update request)."""
        self.client.post('/distribution/', self.good_data)
        response = self.client.put(
            '/distribution/1/',
            self.bad_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
