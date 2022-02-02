from django.test import SimpleTestCase
from django.urls import reverse


class SwaggerTests(SimpleTestCase):

    def test_swagger_ui_response(self):
        response = self.client.get(reverse('docs:swagger-ui'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('text/html', response['content-type'])

    def test_swagger_json_response(self):
        url = reverse('docs:swagger-without-ui', kwargs={'format': '.json'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIn('application/json', response['content-type'])

    def test_swagger_yml_response(self):
        url = reverse('docs:swagger-without-ui', kwargs={'format': '.yaml'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIn('application/yaml', response['content-type'])


class RedocTests(SimpleTestCase):

    def test_redoc_ui_response(self):
        response = self.client.get(reverse('docs:redoc-ui'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('text/html', response['content-type'])
