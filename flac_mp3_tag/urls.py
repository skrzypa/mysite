from django.urls import path


from . import views

app_name = 'flac_mp3_tag'


urlpatterns = [
    path(route= 'flac_mp3_tag/', view= views.automatictagging, name= 'flac_mp3_tag'),
]