from django.contrib import admin
from .models import *

# Register your models here.
class ColorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'chapter_text', 'chapter_color', 'content_text', 'content_color', 'menu_text', 'menu_color', 'alg_text', 'alg_color']
admin.site.register(Colors, ColorsAdmin)