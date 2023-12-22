from django.contrib import admin
from .models import *

# Register your models here.

class AvailableAppAdmin(admin.ModelAdmin):
    list_display = ('id_app', 'app_name', 'app_describe', 'app_link', 'app_log_in')
admin.site.register(AvailableApp, AvailableAppAdmin)



class AppPhotosAdmin(admin.ModelAdmin):
    list_display = ('id_photo', 'id_app', 'photo')
admin.site.register(AppPhotos, AppPhotosAdmin)
    


class NewEventModelAdmin(admin.ModelAdmin):
    """EDIT"""
    list_display = ('id', 'event_title', 'event_location', 'owner', 'event_description', 'event_date_year', 'event_date_month', 'event_date_day')
admin.site.register(NewEventModel, NewEventModelAdmin)



class InvitedToEventModelAdmin(admin.ModelAdmin):
    list_display = ('event', 'invited_friend', 'accepted_invitation')
admin.site.register(InvitedToEventModel, InvitedToEventModelAdmin)



admin.site.register(Friendship)



class AddExpenseGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'expense_title', 'status', 'date_added']
admin.site.register(AddExpenseGroup, AddExpenseGroupAdmin)



class AddFriendToExpenseGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_group_id', 'invited_to_group_friend']
admin.site.register(AddFriendToExpenseGroup, AddFriendToExpenseGroupAdmin)



class AddExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'expense_group_id', 'description', 'price', 'repaid', 'date_added']
admin.site.register(AddExpense, AddExpenseAdmin)


class AddFriendToExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_id', 'expense_group_id', 'invited_to_expense_friend', 'amount', 'to_repayment']
admin.site.register(AddFriendToExpense, AddFriendToExpenseAdmin)



class OpenRegistrationAdmin(admin.ModelAdmin):
    list_display = ["describe", "is_open"]
admin.site.register(OpenRegistration, OpenRegistrationAdmin)



class BeerStylesAdmin(admin.ModelAdmin):
    list_display = ('id', 'style_name', 'max_carbonation', 'min_carbonation')
admin.site.register(BeerStyles, BeerStylesAdmin)