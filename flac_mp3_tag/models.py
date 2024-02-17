from django.db import models

# Create your models here.
class VideoLink(models.Model):
    id = models.AutoField(primary_key= True)
    video_link = models.TextField()