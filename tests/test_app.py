from tests.base import BaseTestCase


class TestApp(BaseTestCase):
    def test_health(self):
        response = self.test_client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})