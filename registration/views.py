from django.conf import settings
from django.contrib.auth import (
    authenticate, login, REDIRECT_FIELD_NAME, logout as auth_logout)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View

from registration.models import User
from registration.forms import UserCreationForm, LoginForm

def logout(request):
    auth_logout(request)
    return redirect('home')

class PasswordResetView(View):
    """
    The view to send a reset email on forgeting password.
    """
    def get(self, request):
        return render(request, 'registration/password_reset.html')
    
    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            message = "You will receive a password reset link shortly at you email {}. If you do not receive it please check yor spam folder and try again.".format(request.POST['email'])
            messages.info(request, message)
            return redirect('home')
        messages.info(request, "Invalid Email!")
        return redirect('home')

class SignUpView(View):
    """
    The view for handling request to /login url.
    Implements get and post methods.
    """
    def get(self, request):
        redirect_to = request.GET.get('next', '')
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {
            'form': form,
            'next': redirect_to,
        })
    
    def post(self, request):
        redirect_to = request.GET.get('next', '')
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(redirect_to)
        else:
            return render(request, 'registration/signup.html', {
                'form': form,
            })

class LoginView(View):

    def get(self, request):
        redirect_to = request.GET.get('next', '')
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        if request.user.is_authenticated:
            return redirect(redirect_to)
        form = LoginForm()
        return render(request, 'registration/login.html', {
            'form': form,
            'next': redirect_to,
        })
    
    def post(self, request):
        redirect_to = request.POST.get(
            REDIRECT_FIELD_NAME,
            request.GET.get('next', '')
        )
        creds = request.POST
        form = LoginForm(creds)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(redirect_to)
        else:
            return render(request, 'registration/login.html', {
                'form': form,
                'next': redirect_to
            })