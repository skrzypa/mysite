from django.contrib import admin
from .models import Note, InvitedToNote

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title', 'content', 'created']
admin.site.register(Note, NoteAdmin)


class InvitedToNoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'note', 'invited_friend']
admin.site.register(InvitedToNote, InvitedToNoteAdmin)