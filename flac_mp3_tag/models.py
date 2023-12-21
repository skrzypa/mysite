from django.db import models

# Create your models here.
    

class DescribeApp(models.Model):
    id_app = models.AutoField(primary_key= True)
    app_name = models.TextField(default= '')
    app_describe = models.TextField(default= '')
    app_link = models.TextField(default= '')
    app_photo = models.ImageField(upload_to= 'homepage/')
    app_link = models.TextField(default= '')
    video_link = models.TextField(default= '')

    class Meta:
        verbose_name = "Describe App"
        verbose_name_plural = "Describe App"