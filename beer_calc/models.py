from django.db import models

# Create your models here.
class BeerStyles(models.Model):
    id = models.AutoField(primary_key= True)
    style_name = models.TextField(default= "")
    max_carbonation = models.FloatField(default= 0)
    min_carbonation = models.FloatField(default= 0)

    class Meta:
        verbose_name = "Beer style"
        verbose_name_plural = "Beer styles"



class ButtonIcon(models.Model):
    id = models.AutoField(primary_key= True)
    photo = models.ImageField(upload_to= f'beer_calc_icon/')

    class Meta:
        verbose_name = "Button Icon"
        verbose_name_plural = "Button Icon"