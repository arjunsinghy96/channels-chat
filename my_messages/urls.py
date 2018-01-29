from django.urls import path
from my_messages import views

urlpatterns = [
        path('', views.home_page, name='home'),
        path('chat/<room>/', views.chat_page, name='chat'),
        path('signup/', views.SignUpView.as_view(), name='signup'),
        path('leagues/', views.LeagueView.as_view(), name='leagues'),
        path('invites/', views.InviteView.as_view(), name='invites'),
        path('accept/<invite_id>', views.accept_invite, name='accept'),
        ]
