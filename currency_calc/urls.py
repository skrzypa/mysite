from django.urls import path


from . import views



app_name = 'currency_calc'
urlpatterns = [
    path('currency_calc/', views.currency_calc, name='currency_calc'),
]