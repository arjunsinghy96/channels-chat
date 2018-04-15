from django.urls import path

from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('league/', views.LeagueView.as_view(), name='league')
]