from django.urls import path, include

from . import views

app_name = 'checklist'

urlpatterns = [
    path('checklist/', view= views.checklist, name= 'checklist'),
    path('checklist_note/<int:id>/', view= views.note, name= 'note'),
]
