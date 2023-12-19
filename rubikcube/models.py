from django.db import models

# Create your models here.


class Colors(models.Model):
    id = models.AutoField(primary_key= True)
    chapter_text = models.TextField(default= "dark")
    chapter_color = models.TextField(default= "#FFFFFF")
    content_text = models.TextField(default= "dark")
    content_color = models.TextField(default= "#FFFFFF")
    menu_text = models.TextField(default= "dark")
    menu_color = models.TextField(default= "#FFFFFF")
    alg_text = models.TextField(default= "dark")
    alg_color = models.TextField(default= "#FFFFFF")

    class Meta:
        verbose_name = "Colors"
        verbose_name_plural = "Colors"
    

class DescribeApp(models.Model):
    id_app = models.AutoField(primary_key= True)
    app_name = models.TextField(default= '')
    app_describe = models.TextField(default= '')
    app_link = models.TextField(default= '')
    app_photo = models.ImageField(upload_to= 'homepage/')

    class Meta:
        verbose_name = "Describe App"
        verbose_name_plural = "Describe App"