from decimal import Decimal
from django.test import TestCase
from django.urls import reverse


class AddTwoNumbersViewTests(TestCase):


    # def test_integer_params(self):
    #     self.assertEqual(3, 2)

    def test_decimal_params(self):
        response = self.client.get(reverse('add-two-numbers'), {
            'first': Decimal(1.25),
            'second': Decimal(1.25),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'result': '2.50',
        })
    # def test_float_params(self):
    #     response = self.client.get(reverse('add-two-numbers'), {
    #         'first': 1.25,
    #         'second': 1.25,
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), {
    #         'result': '2.50',
    #     })
    # def test_params_invalid_type(self):
    #     response = self.client.get(reverse('add-two-numbers'), {
    #         'first': 'test',
    #         'second': 1,
    #     })
    #     self.assertEqual(response.status_code, 400)
    # def test_missing_params(self):
    #     response = self.client.get(reverse('add-two-numbers'), {
    #         'first': 1,
    #     })
    #     self.assertEqual(response.status_code, 400)