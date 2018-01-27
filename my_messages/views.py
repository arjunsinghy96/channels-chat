from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate

from my_messages.forms import LoginForm, SignUpForm
from my_messages.models import League

@login_required(login_url='/login')
def home_page(request):
    if request.method == 'POST':
        room = request.POST['room']
        username = request.POST['username']
        request.session['username'] = username
        return redirect('chat', permanent=True, room=room)
    return render(request, 'home.html')

@login_required(login_url='/login')
def chat_page(request, room):
    league, created  = League.objects.get_or_create(name='chat-%s'%room)
    messages = league.messages.all().order_by('-timestamp')
    return render(request, 'chat.html',
            {
                'username': request.user.username,
                'messages': messages,
            }
        )

class LoginView(View):

    def get(self, request):
        form  = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        user = request.POST
        user = authenticate(username=user['username'],
                            password=user['password1'])
        login(request, user)
        return redirect('home')

class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leagues', permanent=True)

class LeagueView(View):

    def get(self, request):
        leagues = League.objects.all()
        return render(request, 'leagues.html', {'leagues': leagues})
