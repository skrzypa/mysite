from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Note(models.Model):
    id = models.AutoField(primary_key= True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)
    title = models.TextField(blank= False, max_length= 50)
    content = models.JSONField(default= dict)
    created = models.DateTimeField(default= timezone.now)


    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"


    def __str__(self):
        return f"{self.id}. owner = {self.owner.username}, title = {self.title}"



class InvitedToNote(models.Model):
    id = models.AutoField(primary_key= True)
    note = models.ForeignKey(to= Note, on_delete= models.CASCADE)
    invited_friend = models.ForeignKey(to= User, on_delete= models.CASCADE)


    class Meta:
        verbose_name = 'Invited to note'
        verbose_name_plural = 'Invited to note'
    

    def __str__(self):
        return f"{self.id}. {self.invited_friend} added to {self.note.title}"