from django.contrib import admin
from .models import BeerStyles

# Register your models here.
class BeerStyleAdmin(admin.ModelAdmin):
    list_display = ['id', 'style_name', 'min_carbonation', 'max_carbonation']
admin.site.register(BeerStyles, BeerStyleAdmin)