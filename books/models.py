from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewBook(models.Model):
    id = models.AutoField(primary_key= True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE, null= True, blank=True)
    title = models.TextField(default= "")
    author = models.TextField(default= "")
    link_to_cover = models.TextField(default= "")
    date = models.DateField(default= "")
    date_added = models.DateTimeField(auto_now_add= True) # przy migracji timezone.now

    def __str__(self):
        if len(self.title) <=15:
            t = self.title
        else:
            t = self.title[:16] + "..."

        if len(self.author) <=15:
            a = self.author
        else:
            a = self.author[:16] + "..."


        return f"{self.id}. {t} by {a}"