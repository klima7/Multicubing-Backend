from django.test import TestCase


class AnimalTestCase(TestCase):

    # def test_fail(self):
    #     """Animals that can speak are correctly identified"""
    #     self.assertEqual(2, 1)

    def test_success(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(1, 1)
