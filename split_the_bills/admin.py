from django.contrib import admin
from .models import SplitTheBills, AddToGroup

# Register your models here.
class SplitTheBillsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'bills', 'created')
admin.site.register(SplitTheBills, SplitTheBillsAdmin)



class AddToGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'added_user',)
admin.site.register(AddToGroup, AddToGroupAdmin)