from django.contrib import admin

from storage.models import League, Membership, Message, Invite

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('league', 'user', 'permissions', 'joined_at')

@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ('league', 'sender', 'sent_at')

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('league', 'user', 'permissions')
