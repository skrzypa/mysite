"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('homepage.urls')),     # dodajemy url naszej apki
    # path('', include('meetings.urls')),     # dodajemy url naszej apki
    # path('', include('users.urls')),        # dodajemy url naszej apki
    # path('', include('beer_calc.urls')),        # dodajemy url naszej apki
    path('', include('my_apps.urls')),        # dodajemy url naszej apki
    path('', include('password_generator.urls')),        # dodajemy url naszej apki
    path('', include('currency_calc.urls')),        # dodajemy url naszej apki
    path('', include('rubikcube.urls')),        # dodajemy url naszej apki
    path('', include('flac_mp3_tag.urls')),        # dodajemy url naszej apki
    path('', include('deploying.urls')),        # dodajemy url naszej apki
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)