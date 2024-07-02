from django.contrib import admin
from .models import Note

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title', 'content', 'invited_friends', 'date_added']
admin.site.register(Note, NoteAdmin)