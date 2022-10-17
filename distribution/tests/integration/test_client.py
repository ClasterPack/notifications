from django.test import Client, TestCase


class ClientTest(TestCase):
    """Создаем TestCase."""

    def setUp(self):
        """Настраиваем для проверки запросов. Создаем Клиент для отправки запросов со стороны клиента."""
        self.client = Client()
        self.data = {
            'phone_number': 79994998877,
            'operator_code': 999,
            'tag': 'test_tag',
            'timezone': 'UTC',
        }
        self.data_check = {
            'id': 1,
            'phone_number': '79994998877',
            'operator_code': '999',
            'tag': 'test_tag',
            'timezone': 'UTC',
        }

    def test_crud(self):
        """Проверяем CREATE READ UPDATE DELETE Http запросы к API клиента."""
        response_get = self.client.get('/clients/')
        self.assertEqual(response_get.status_code, 200)
        response_post = self.client.post('/clients/', self.data)
        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_post.data, self.data_check)
        response_put = self.client.put('/clients/1/', self.data, content_type='application/json')
        self.assertEqual(response_put.status_code, 200)
        response_delete = self.client.delete('/clients/1/')
        self.assertEqual(response_delete.status_code, 204)

    def test_wrong_post(self):
        """Проверяем неверный POST запрос к клиенту."""
        data = {
            'test_tag': 'test_tag',
        }
        response = self.client.post('/clients/', data)
        self.assertEqual(response.status_code, 400)

    def test_get_detail(self):
        """Проверяем реквест GET для клиента."""
        post_request = self.client.post('/clients/', self.data)
        response = self.client.get('/clients/1/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.data_check)

    def test_bad_put_request(self):
        """Проверям реквест на обновление клиента с неверным датасетом."""
        new_data = {'tests': 'bad data'}
        post_request = self.client.post('/clients/', self.data)
        response = self.client.put('/clients/1/', new_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
