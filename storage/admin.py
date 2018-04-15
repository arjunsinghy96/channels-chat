from django.contrib import admin

from storage.models import League, Membership

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
