# mysite
## Several web applications in Django, including a meeting planner with friends and a split bills aplication

Django 4.1.7  
django-bootstrap-v5 1.0.11  
Python 3.11.1  

## In my_site.py add:
```
urlpatterns = [
    ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## In settings.py add:
```
INSTALLED_APPS = [
    # my applications
    'my_apps',
    'password_generator',

    # external applications
    'bootstrap5',

    # default applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

STATICFILES_DIRS = [
    (os.path.join(BASE_DIR, 'static')),
    ]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '/static/'
```

## To do:  
1. Refactoring the whole views.py

Split the bills:
1. Better group summary
1. ??? Sending an email with a link to the group, if you are invited, and any expenses that apply to you

Beer calc
1. Find formula for beer carbonation

Meeting planner
1. Past event on the calendar

Currency cal
1. New application without login - currency calculator with NBP API