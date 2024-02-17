from django.contrib import admin

from .models import *
# Register your models here.
class VideoLinkAmin(admin.ModelAdmin):
    list_display = ['id', 'video_link']
admin.site.register(VideoLink, VideoLinkAmin)