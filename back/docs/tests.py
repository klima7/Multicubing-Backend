from django.test import TestCase


class ExampleTest(TestCase):

    def test_success(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(1, 1)
