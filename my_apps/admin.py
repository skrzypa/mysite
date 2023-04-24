from django.contrib import admin
from .models import *

# Register your models here.

class NewEventModelAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'event_location', 'owner', 'event_description', 'event_date_year', 'event_date_month', 'event_date_day')
admin.site.register(NewEventModel, NewEventModelAdmin)

class InvitedToEventModelAdmin(admin.ModelAdmin):
    list_display = ('event', 'invited_friend', 'accepted_invitation')
admin.site.register(InvitedToEventModel, InvitedToEventModelAdmin)


admin.site.register(Friendship)