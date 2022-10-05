from django.test import TestCase
from django.urls import reverse
from mock import patch


class HelloTests(TestCase):
    def test_contains_hello(self):
        args = ['Ania']
        #response = self.client.get(reverse('hello_world_with_name', args={'name': 'Ania'}))
        response = self.client.get(reverse('hello_world_with_name', args=args))
        self.assertEqual(response.status_code, 200)
        # html = response.getvalue()
        # htmlString = html.decode('utf-8')
        # print(htmlString)
        # self.assertIn("Hello", htmlString)
        self.assertContains(response, "Hello", html=False)
        #self.assertContains(response, "<h1>Hello  Ania</h1>", html=True)

    def test_contain_url_parameter(self):
        arg = 'Ania'
        response = self.client.get(reverse('hello_world_with_name', args= [arg]))
        self.assertContains(response, arg)




