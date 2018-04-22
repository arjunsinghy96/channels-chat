import csv

from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from website.forms import LeagueForm
from storage.models import League, Membership, Invite, Notification
from registration.models import User

permissions = {
    'owner': '4',
    'master': '3',
    'member': '2',
    'guest': '1',
}

@staff_member_required
@require_POST
def upload_membership_csv(request):
    if request.POST:
        fieldnames = ['league_name', 'username', 'permissions']
        reader = csv.DictReader(request.FILES['membership'].read().decode('utf-8').splitlines())
        errors = []
        count = 0
        for row in reader:
            try:
                league = League.objects.get(name=row['league_name'])
                user = User.objects.get(username=row['username'])
                membership = Membership.objects.get_or_create(
                    league=league,
                    user=user,
                    permissions=permissions[row['permissions']]
                )
                count += 1
            except:
                errors.append(row)
        return render(request, 'admin/membership_csv_uploaded.html',{
            'count': count,
            'errors': errors,
        })

class UserDatasetView(View):

    @method_decorator(staff_member_required)
    def get(self, request):
        return render(request, 'admin/users_csv_upload.html')

    @method_decorator(staff_member_required)
    def post(self, request):
        print(request.FILES['user_dataset'])
        fieldnames = ['username', 'email', 'first_name', 'last_name', 'phone_no', 'is_staff', 'password']
        reader = csv.DictReader(request.FILES['user_dataset'].read().decode('utf-8').splitlines())
        errors = []
        count =0 
        for row in reader:
            try:
                user = User.objects.create(
                    username=row['username'],
                    email=row['email'],
                    phone_no=row['phone_no'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    is_staff=True if row['is_staff'] == '1' else False,
                    is_active=True
                )
                user.set_password(row['password'])
                user.save()
                count += 1
            except IntegrityError:
                errors.append(row)
            
        return render(request, 'admin/users_csv_uploaded.html', {
            'count': count,
            'errors': errors,
        })


def search_user(request):
    q = request.GET.get('q', '')
    if not q:
        return JsonResponse([], safe=False)
    users = User.objects.only('username').filter(
                                              username__icontains=q)[:10]
    usernames = [user.username for user in users]
    return JsonResponse(usernames, safe=False)

def search_league(request):
    q = request.GET.get('q', '')
    if not q:
        return JsonResponse([], safe=False)
    leagues = League.objects.only('name').filter(
                                              name__icontains=q)[:10]
    leagues = [league.name for league in leagues]
    return JsonResponse(leagues, safe=False)

@login_required
@require_POST
def update_phone(request):
    if request.POST:
        post = request.POST
        print(post)
        number = post['country'] + post['number']
        request.user.phone_no = number
        request.user.save()
        return redirect('profile')

@login_required
@require_POST
def update_name(request):
    if request.POST:
        name = request.POST
        request.user.first_name = name['first_name']
        request.user.last_name = name['last_name']
        request.user.save()
        return redirect('profile')

@login_required
def kick_member(request, member_id, league_id):
    if request.user.id == member_id:
        messages.info(request, 'Cannot kick yourself')
        return redirect('dashboard')
    try:
        perms = Membership.objects.get(user=request.user, league=league_id)
        print(perms.can_kick())
        if perms.can_kick():
            try:
                membership = Membership.objects.get(user=member_id, league=league_id)
                membership.delete()
                return redirect('league_detail', id=league_id)
            except:
                raise Http404
        else:
            raise PermissionDenied
    except Membership.DoesNotExist:
        raise PermissionDenied

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
        notifications = Notification.objects.order_by('-timestamp')[:20]
        form = LeagueForm()
        return render(request, 'website/dashboard.html', {
            'leagues': leagues,
            'form': form,
            'notifications': notifications,
            })

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
            kick_perm = Membership.objects.get(league=league, user=request.user).get_permissions_display()
            return render(request, 'website/league.html', {
                'league': league,
                'members': members,
                'kick_perm': kick_perm,
            })
        except League.DoesNotExist:
            messages.info(request, 'This league does not exist')
            return redirect('dashboard')
        except Membership.DoesNotExist:
            messages.info(request, 'Forbidden: Not member')
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
        invite.permissions = permissions
        invite.save()
        return redirect('league_detail', id=league.pk)