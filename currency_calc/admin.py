from django.contrib import admin
from .models import NBP_API

# Register your models here.
class NBP_APIAdmin(admin.ModelAdmin):
    list_display = ['id', 'currencies', 'date_addded']
admin.site.register(NBP_API, NBP_APIAdmin)