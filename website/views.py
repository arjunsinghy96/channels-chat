from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views import View

from website.forms import LeagueForm
from storage.models import League, Membership, Invite
from registration.models import User

@login_required
def accept_invite(request, id):
    try:
        invite = Invite.objects.get(pk=id)
        if invite.user == request.user:
            mem, created = Membership.objects.update_or_create(
                league=invite.league,
                user=invite.user
                )
            if created:
                mem.permissions = invite.permissions
                mem.save()
            elif mem.permissions < invite.permissions:
                mem.permissions = invite.permissions
                mem.save()
            invite.delete()
        else:
            messages.info(request, 'Unauthorized')
        return redirect('invites')
    except Invite.DoesNotExist:
        messages.info(request, 'Invite does not exist')
        return redirect('invites')

@login_required
def reject_invite(request, id):
    try:
        invite = Invite.objects.get(pk=id)
        if invite.user == request.user:
            invite.delete()
        else:
            messages.info(request, 'Unauthorized')
        return redirect('invites')
    except Invite.DoesNotExist:
        messages.info(request, 'Invite does not exist')
        return redirect('invites')

@login_required
def chat_page(request, slug):
    try:
        league = League.objects.get(slug=slug)
        membership = Membership.objects.get(
            user=request.user,
            league=league,
        )
        messages = league.messages.all().order_by('sent_at')
        return render(request, 'website/chat.html', {
            'league': league,
            'membership': membership,
            'messages': messages,
        })
    except Membership.DoesNotExist:
        return redirect('home')
    except League.DoesNotExist:
        return redirect('home')

@login_required
def invite_count(request):
    count = Invite.objects.filter(user=request.user).count()
    return JsonResponse({'count': count}, status=200)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'website/profile.html')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        leagues = request.user.member_of.all()
        form = LeagueForm()
        return render(request, 'website/dashboard.html', {'leagues': leagues, 'form': form})

class LeagueView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            post = request.POST
            league = League.objects.create(
                name=post['name'],
                slug=slugify(post['name'])
            )
            Membership.objects.create(
                league=league,
                user=request.user,
                permissions='4',
            )
            messages.info(request, 'New league created')
        except:
            messages.info(request, 'League already exists')
        return redirect('dashboard')

class LeagueDetailsView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            league = League.objects.get(pk=id)
            members = league.members.all()
            return render(request, 'website/league.html', {
                'league': league,
                'members': members,
            })
        except League.DoesNotExist:
            messages.info('This league does not exist')
            return redirect('dashboard')

class InvitesView(LoginRequiredMixin, View):
    def get(self, request):
        invites = Invite.objects.filter(user=request.user)
        return render(request, 'website/invites.html', {
            'invites': invites,
        })

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
        return redirect('league_detail', id=league.pk)