from django.contrib import admin
from my_messages.models import League, Message, Membership

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('league', 'sender', 'message')

@admin.register(Membership)
class Membership(admin.ModelAdmin):
    list_display = ('league', 'user', 'joined_at')
