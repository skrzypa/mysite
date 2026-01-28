from django.contrib import admin
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from .models import *

# Register your models here.

class NewBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'author', 'link_to_cover', 'date', 'date_added')
admin.site.register(NewBook, NewBookAdmin)