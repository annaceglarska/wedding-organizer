from django.test import TestCase
from django.urls import reverse


class HelloTests(TestCase):
   def test_contains_hello(self):
       response = self.client.get(reverse('hello_world_with_name', args={'name': 'Ania'}))
       self.assertEqual(response.status_code, 200)
       html = response.getvalue()
       self.assertEqual(html.find('Ania') > -1, True)
       self.assertEqual(html.find('Grzegorz') > -1, False)




