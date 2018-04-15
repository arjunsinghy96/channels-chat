from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from website.forms import LeagueForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        leagues = request.user.member_of.all()
        form = LeagueForm()
        return render(request, 'website/dashboard.html', {'leagues': leagues, 'form': form})