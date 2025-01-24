from django.urls import path, include

from . import views

app_name = 'beer_calc'

urlpatterns = [
    path('beer_calc/', views.beer_calc, name= 'beer_calc')
]