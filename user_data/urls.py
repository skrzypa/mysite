from django.urls import path


from . import views



app_name = 'user_data'
urlpatterns = [
    path(route= 'user_data/', view= views.user_data, name= 'user_data'),
]