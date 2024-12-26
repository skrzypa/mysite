from django.db import models
from django.contrib.auth.models import User 



# Create your models here.
class SplitTheBills(models.Model):
    id = models.AutoField(primary_key= True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)
    title = models.TextField(default= "", blank= False)
    bills = models.JSONField(default= dict)
    created = models.DateTimeField()
    status = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.id}. {self.title}"
    
    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = "Split the bills"
        verbose_name_plural = "Split the bills"



class AddToGroup(models.Model):
    id = models.AutoField(primary_key= True)
    group = models.ForeignKey(to= SplitTheBills, on_delete= models.CASCADE)
    added_user = models.ForeignKey(to= User, on_delete= models.CASCADE)

    class Meta:
        verbose_name = "Add to group"
        verbose_name_plural = "Add to group"



