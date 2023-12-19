from django.urls import path


from . import views



app_name = 'rubikcube'
urlpatterns = [
    path('rubik_cube/', views.rubiccube, name='rubikcube'),
]