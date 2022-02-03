from django.test import SimpleTestCase
from django.urls import reverse


class IndexTests(SimpleTestCase):

    def test_index_page_status_code(self):
        response = self.client.get(reverse('index:index'))
        self.assertEquals(response.status_code, 200)
