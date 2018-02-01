from django.test import TestCase
from django.urls import resolve
from my_messages import views

class HomePageTest(TestCase):

    def test_root_maps_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_page_redirects_to_login(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/')


class ChatPageTest(TestCase):
    
    def test_chat_maps_to_chat_page_view(self):
        found = resolve('/chat/room1/')
        self.assertEqual(found.func, views.chat_page)
        found = resolve('/chat/room2/')
        self.assertEqual(found.func, views.chat_page)
