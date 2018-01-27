from django.contrib import admin
from my_messages.models import League, Message, Membership
from my_messages.models import Invite

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('league', 'sender', 'message')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('league', 'user', 'joined_at')

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('user', 'league')
