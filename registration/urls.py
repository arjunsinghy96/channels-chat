from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

from registration import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
        ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
        ),
]
