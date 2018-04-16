from django.urls import path

from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('league/', views.LeagueView.as_view(), name='league'),
    path('invites/', views.InvitesView.as_view(), name='invites'),
    path('invite/<int:id>/accept/', views.accept_invite, name="invite_accept"),
    path('invite/<int:id>/reject/', views.reject_invite, name="invite_reject"),
    path('invites/count/', views.invite_count, name='invite_count'),
    path('chat/<slug:slug>/', views.chat_page, name='chat'),
    path('league/<int:id>/details/', views.LeagueDetailsView.as_view(), name='league_detail'),
]