from django.urls import path


from . import views

app_name = 'password_generator'
urlpatterns = [
    path('password_generator/', views.password_generator, name='password_generator'),
]