from django.urls import path

from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('league/', views.LeagueView.as_view(), name='league'),
    path('invites/count/', views.invite_count, name='invite_count'),
    path('chat/<slug:slug>/', views.chat_page, name='chat'),
    path('league/<int:id>/details/', views.LeagueDetailsView.as_view(), name='league_detail'),
]