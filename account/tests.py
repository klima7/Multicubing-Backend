from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTests(APITestCase):

    def _register(self, email, username, password):
        url = reverse('api:Account-register')
        data = {
            'email': email,
            'username': username,
            'password': password
        }
        return self.client.post(url, data, format='json')

    def test_register_success_when_valid(self):
        response = self._register('user@gmail.com', 'superuser', 'password123')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_fail_when_invalid_email(self):
        response = self._register('email', 'superuser', 'password123')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fail_when_username_too_short(self):
        response = self._register('user@gmail.com', '1234', 'password123')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fail_when_username_contains_at(self):
        response = self._register('user@gmail.com', 'superuser@', 'password123')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fail_when_email_exists(self):
        response = self._register('user@gmail.com', 'superuser', 'password123')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self._register('user@gmail.com', 'foobar', 'password123')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
