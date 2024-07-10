from django.urls import path


from . import views



app_name = 'currency_calc'
urlpatterns = [
    # path('currency_calc/', views.currency_calc, name='currency_calc'),
    # path('currency_calc/<str:parametr_result>/<str:parametr_message>/', views.currency_calc, name='currency_calc_with_params'),
    
    path('currency_calc/', views.currency_calc, name='currency_calc'),
    path('currency_calc/<str:date>', views.currency_calc, name='currency_calc'),
    path('currency_calc_records/', views.records, name='currency_calc_records'),
    path('currency_calc_sources/', views.sources, name='currency_calc_sources'),
    path('currency_calc_plots/', views.plots, name='currency_calc_plots'),
]