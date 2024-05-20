from django.db import models

# Create your models here.
class NBP_API(models.Model):
    id = models.AutoField(primary_key= True)
    date_addded = models.DateTimeField(auto_now= True)
    currencies = models.JSONField()