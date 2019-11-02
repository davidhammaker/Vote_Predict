from django.urls import reverse
from rest_framework.test import APITestCase


class RootIndexTests(APITestCase):
    url = reverse('root-index')

    def test_get_root(self):
        """
        Users can access Root Index.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
