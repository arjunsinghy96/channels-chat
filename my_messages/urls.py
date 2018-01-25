from django.urls import path
from my_messages import views

urlpatterns = [
        path('', views.home_page, name='home'),
        path('chat/<room>/', views.chat_page, name='chat'),
        ]
