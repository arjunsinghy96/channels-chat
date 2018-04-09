from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from my_messages.forms import LoginForm, SignUpForm, LeagueForm
from my_messages.models import League, Invite, Message, Membership

@login_required
def home_page(request):
    return redirect('leagues')

@login_required
def chat_page(request, room):
    league, created  = League.objects.get_or_create(name=room)
    try:
        membership = Membership.objects.get(
            user=request.user,
            league=league,
        )
    except Membership.DoesNotExist:
        return render(request, 'not_member.html')
    messages = league.messages.all().order_by('timestamp')
    return render(request, 'chat.html',
            {
                'username': request.user.username,
                'messages': messages,
                'league_name': room,
                'membership': membership,
            }
        )

@login_required
def accept_invite(request, invite_id):
    invite = Invite.objects.get(pk=invite_id)
    mem, created = Membership.objects.update_or_create(league=invite.league,
                                        user=invite.user)
    if created:
        mem.permissions = invite.permissions
        mem.save()
    elif mem.permissions < invite.permissions:
        mem.permissions = invite.permissions
        mem.save()
    invite.delete()
    return redirect('leagues', permanent=True)

class LoginView(View):

    def get(self, request):
        form  = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        user = request.POST
        user = authenticate(username=user['username'],
                            password=user['password1'])
        login(request, user)
        return redirect('leagues')

class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leagues', permanent=True)
        return render(request, 'signup.html', {'form': form})

class LeagueView(LoginRequiredMixin, View):

    def get(self, request):
        leagues = request.user.member_of.all()
        form = LeagueForm()
        return render(request, 'leagues.html', {'leagues': leagues, 'form': form})

    def post(self, request):
        form = LeagueForm(request.POST)
        if form.is_valid():
            room = request.POST['name']
            league, created = League.objects.get_or_create(name=room)
            if created:
                Membership.objects.create(league=league,
                                          user=request.user,
                                          permissions='4')
            return redirect('chat', permanent=True, room=room)

class InviteView(LoginRequiredMixin, View):

    def get(self, request):
        invites = request.user.invite_set.all()
        return render(request, 'invites.html', {'invites': invites})

    def post(self, request):
        username = request.POST['username']
        permissions = request.POST['permissions']
        invited = User.objects.get(username=username)
        league = League.objects.get(name=request.POST['league_name'])
        invite, created = Invite.objects.get_or_create(user=invited,
                                              league=league)
        print(permissions)
        invite.permissions = permissions
        invite.save()
        print(invite.permissions)
        return render(request, 'invite_sent.html')
