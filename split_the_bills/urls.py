from django.urls import path


from . import views

app_name = 'split_the_bills'
urlpatterns = [
    path('split_the_bills/', views.split_the_bills, name='split_the_bills'),
    path('split_the_bills_group/<int:group_id>', views.split_the_bills_group, name='split_the_bills_group'),
]