from django.urls import path
from django.contrib import admin


from . import views

app_name = 'my_apps'
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('beer_calc/', views.calc, name='beer_calc'),
    path('', views.index, name='homepage'),
    #path('meetings_calendar/', views.meetings_homepage_old, name='meetings_calendar'),
    path('meetings_calendar/', views.meetings_homepage, name='meetings_calendar'),
    path('meetings_edit_event/<str:event_id>/', views.edit_event, name='meetings_edit_event'),
    path('meetings_new_event/<str:date>/', views.new_event, name='meetings_new_event'),
    #path('meetings_new_event/', views.new_event, name='meetings_new_event'),
    #path('meetings_new_event/', views.new_event_old, name='meetings_new_event'),
    path('users_friends/', views.friends, name='users_friends'),
    path('users_log_in/', views.log_in, name='users_log_in'),
    path('users_log_out/', views.log_out, name='users_log_out'),
    path('users_register/', views.register, name='users_register'),
    path('split_homepage/', views.add_expense_group, name='split_homepage'),
    path('split_group/<int:group_id>/', views.split_group, name='split_group'), 
]