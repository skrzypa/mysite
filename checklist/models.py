from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    id = models.AutoField(primary_key= True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)
    title = models.TextField(blank= False, max_length= 50)
    content = models.JSONField(default= dict)
    invited_friends = models.JSONField(default= dict)
    date_added = models.DateTimeField(auto_now= True)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"