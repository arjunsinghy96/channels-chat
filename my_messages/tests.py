from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve
from my_messages import views

class HomePageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                        password='test_user')

    def test_root_maps_to_home_page_view(self):
        """
        Test that the home_page view is used to respond on root path
        """
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_page_redirects_to_login(self):
        """
        Test that the home page redirects to the login page if user is not
        logged in.
        """
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_home_page_redirects_to_leagues_page(self):
        """
        Tests that the home page redirects to the leagues page when the 
        user is logged in.
        """
        self.client.login(username='test_user', password='test_user')
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/leagues/')


class ChatPageTest(TestCase):
    
    def test_chat_maps_to_chat_page_view(self):
        """
        Tests that the chat_page view is used to resond on /chat path with
        different room names.
        """
        found = resolve('/chat/room1/')
        self.assertEqual(found.func, views.chat_page)
        found = resolve('/chat/room2/')
        self.assertEqual(found.func, views.chat_page)

    def test_home_page_redirects_to_login(self):
        """
        Test that the chat page redirects to login page if user is not
        logged in.
        """
        response = self.client.get('/chat/room1/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/chat/room1/')
