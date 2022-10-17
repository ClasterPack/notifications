from django.test import Client, TestCase


class TestMessage(TestCase):
    """TestCase для сообщений."""

    def setUp(self):
        """Настройка клиента и данные для проверки запрсов."""
        self.client = Client()
        self.good_data = {
            'status': 'pending',
            'client_id': 1,
            'distribution_id': 2,
        }
        self.bad_data = {
            'tests': 'tests',
        }

    def test_get(self):
        """Тест get запроса на список сообщений."""
        response = self.client.get('/messages/')
        self.assertEqual(response.status_code, 200)

    def test_post_put_delete(self):
        """Тест post запроса."""
        response = self.client.post('/messages/', self.good_data)
        self.assertEqual(response.status_code, 201)
        put_response = self.client.put('/messages/1/', self.good_data, content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        delete_response = self.client.delete('/messages/1/')
        self.assertEqual(delete_response.status_code, 204)

    def test_get_detail(self):
        """Тест детального get запроса ."""
        self.client.post('/messages/', self.good_data)
        response = self.client.get('/messages/1/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], self.good_data['status'])
        self.assertEqual(response.data['client_id'], self.good_data['client_id'])
        self.assertEqual(response.data['distribution_id'], self.good_data['distribution_id'])
