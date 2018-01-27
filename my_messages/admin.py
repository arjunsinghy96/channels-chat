from django.contrib import admin
from my_messages.models import League, Message

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('league', 'handle', 'message')
