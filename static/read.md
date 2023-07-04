# in settings.py:
```
TEMPLATES = [  
    {  
        ...  
        'DIRS': [BASE_DIR / 'templates'],  
        ...  
```

```
# Static files (CSS, JavaScript, Images)  
# https://docs.djangoproject.com/en/4.1/howto/static-files/  
  
STATIC_URL = 'static/'  
  
MEDIA_URL = 'mysite/'  
STATICFILES_DIRS = [  
    (os.path.join(BASE_DIR, 'mysite/static')),  
    ]  
  
MEDIA_ROOT =  BASE_DIR / 'static/mysite'  
STATIC_ROOT = BASE_DIR / 'staticfiles'  
```


# to create this folder use in terminal:
```
python manage.py collectstatic  
```