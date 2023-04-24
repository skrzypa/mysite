from django.urls import path


from . import views

app_name = 'my_apps'
urlpatterns = [
    path('admin/', views.calc, name='admin'),
    path('beer_calc/', views.calc, name='beer_calc'),
    path('contact/', views.contact, name='contact'),
    path('', views.index, name='index'),
    path('meetings_calendar/', views.calendar_generate, name='meetings_calendar'),
    path('meetings_edit_event/<int:id>/', views.edit_event, name='meetings_edit_event'),
    path('meetings_new_event/', views.new_event, name='meetings_new_event'),
    path('users_friends/', views.friends, name='users_friends'),
    path('users_log_in/', views.log_in, name='users_log_in'),
    path('users_log_out/', views.log_out, name='users_log_out'),
    path('users_register/', views.register, name='users_register'),
]