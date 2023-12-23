from django.contrib import admin

from .models import *
# Register your models here.

class DescribeAppAdmin(admin.ModelAdmin):
    list_display = ('id_app', 'app_name', 'app_describe', 'app_photo', 'app_link')
admin.site.register(DescribeApp, DescribeAppAdmin)