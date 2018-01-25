from django.test import TestCase
from django.urls import resolve
from my_messages import views

class HomePageTest(TestCase):

    def test_root_maps_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
