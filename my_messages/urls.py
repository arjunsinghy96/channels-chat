from django.urls import path
from my_messages import views

urlpatterns = [
        path('', views.home_page, name='home'),
        path('chat/<room>/', views.chat_page, name='chat'),
        path('login/', views.LoginView.as_view(), name='login'),
        path('signup/', views.SignUpView.as_view(), name='signup'),
        path('leagues/', views.LeagueView.as_view(), name='leagues'),
        ]
