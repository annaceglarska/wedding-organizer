from django.test import TestCase
from django.urls import reverse
from guestFactory import GuestExapmleTest
from mock import patch


class GuestListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        person1 = [1, "Ernest", "Lasek", 543765876, 25]
        person2 = [2, "Aleksandra", "Kaczmarek", 543321432, 24]

    def test_status_code_is_200(self):
        response = self.client.get(reverse('guest-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('guest-list'))
        self.assertTemplateUsed(response, 'guest_list.html')

    def test_column_name(self):
        columnName = ["Name"]
        response = self.client.get(reverse('guest-list'))
        for one_column in columnName:
            self.assertContains(response, one_column)

    def test_number_of_columns(self): # self czy client ?
        guests = GuestExapmleTest.build()
        with patch.object()