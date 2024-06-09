from django.contrib import admin
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from .models import *

# Register your models here.

class AvailableAppAdmin(admin.ModelAdmin):
    list_display = ('id_app', 'app_name', 'app_describe', 'app_link', 'app_log_in', 'app_tutorial')
admin.site.register(AvailableApp, AvailableAppAdmin)



class AppPhotosAdmin(admin.ModelAdmin):
    actions = ['del_entry_and_photo_file']

    @admin.action(description= "Delete entry and photo file")
    def del_entry_and_photo_file(self, request: WSGIRequest, queryset: QuerySet):
        for obj in queryset:
            obj: AppPhotos
            
            image: ImageFieldFile = getattr(obj, 'photo')
            image.delete()

            obj.delete()
            
        self.message_user(
            request,
            f"Deleted entries and photos: {queryset.count()}",
        )


    list_display = ('id_photo', 'id_app', 'photo')
admin.site.register(AppPhotos, AppPhotosAdmin)
    


class NewEventModelAdminNew(admin.ModelAdmin):
    """EDIT""", 
    list_display = ('id', 'event_title', 'event_location', 'owner', 'event_description', 'event_date', 'event_time', 'date_added')
admin.site.register(NewEventModelNew, NewEventModelAdminNew)


class InvitedToEventModelAdminNew(admin.ModelAdmin):
    list_display = ('id', 'event', 'invited_friend', 'accepted_invitation', 'decline_invitation')
admin.site.register(InvitedToEventModelNew, InvitedToEventModelAdminNew)



class FriendshipClass(admin.ModelAdmin):
    list_display = ('from_friend', 'to_friend')
admin.site.register(Friendship, FriendshipClass)



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