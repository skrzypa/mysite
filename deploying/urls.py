from django.urls import path


from . import views

app_name = 'deploying'

urlpatterns = [
    path('deploying/', views.deploying, name='deploying'), 
]