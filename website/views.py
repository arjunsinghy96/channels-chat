from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views import View

from website.forms import LeagueForm
from storage.models import League, Membership, Invite

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
