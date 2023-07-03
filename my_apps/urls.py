from django.urls import path


from . import views

app_name = 'my_apps'
urlpatterns = [
    path('admin/', views.calc, name='admin'),
    path('beer_calc/', views.calc, name='beer_calc'),
    path('', views.index, name='index'),
    path('meetings_calendar/', views.calendar_generate, name='meetings_calendar'),
    path('meetings_edit_event/<int:id>/', views.edit_event, name='meetings_edit_event'),
    path('meetings_new_event/', views.new_event, name='meetings_new_event'),
    path('users_friends/', views.friends, name='users_friends'),
    path('users_log_in/', views.log_in, name='users_log_in'),
    path('users_log_out/', views.log_out, name='users_log_out'),
    path('users_register/', views.register, name='users_register'),
    path('split_homepage/', views.add_expense_group, name='split_homepage'),
    path('split_group/<int:group_id>/', views.split_group, name='split_group'), 
]