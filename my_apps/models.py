from django.db import models

from django.contrib.auth.models import User # powiążemy wpis z danym użytkownikiem
from django.utils import timezone

# Create your models here.

class AvailableApp(models.Model):
    id_app = models.AutoField(primary_key= True)
    app_name = models.TextField(default= '')
    app_describe = models.TextField(default= '')
    app_link = models.TextField(default= '')
    app_log_in = models.BooleanField(default= True)
    app_tutorial = models.BooleanField(default= False)

    def __str__(self) -> str:
        return f"id: {self.id_app}, name: {self.app_name}"



class AppPhotos(models.Model):
    """  500 x 500 px"""
    id_photo = models.AutoField(primary_key= True)
    id_app = models.ForeignKey(to= AvailableApp, on_delete= models.CASCADE)
    photo = models.ImageField(upload_to= f'homepage/')



class NewEventModel(models.Model):
    """ Wydarzenie tworzone przez użytkownika """
    owner = models.ForeignKey(User, on_delete= models.CASCADE) # powiążemy wpis z danym użytkownikiem

    event_title = models.CharField(max_length= 20, default= "")
    event_location = models.CharField(max_length= 20, default= "")
    event_description = models.CharField(max_length= 200, default= "")
    event_date_year = models.CharField(max_length= 4, default= "") #DELETE
    event_date_month = models.CharField(max_length= 2, default= "") #DELETE
    event_date_day = models.CharField(max_length= 2, default= "") #DELETE

    event_date = models.DateTimeField(auto_now_add= False)

    date_added = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.event_title



class InvitedToEventModel(models.Model):
    event = models.ForeignKey(NewEventModel, on_delete=models.CASCADE)
    invited_friend = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted_invitation = models.BooleanField(default= False) # 1 - przyjął; 0 - brak odp./odrzucił
    decline_invitation = models.BooleanField(default= False) # 1 - odrzucił; 0 - brak odp./przyjął



class Friendship(models.Model):
    from_friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'from_friends')
    to_friend = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'friends')

    all_users = User.objects.all()

    class Meta:
        # Dzięki temu ograniczeniu, nie będzie można dodać do bazy danych dwóch obiektów "Friendship" 
        # z tymi samymi wartościami pól "from_friend" i "to_friend
        unique_together = ('from_friend', 'to_friend')  

    # def __str__(self):
    #     return f"{self.from_friend} add {self.to_friend} to friend"



class AddExpenseGroup(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete= models.CASCADE)
    expense_title = models.CharField(max_length= 100, default= "")
    status = models.CharField(max_length=15, default="Brak wydatków")

    date_added = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f"{self.id}. {self.expense_title}"



class AddFriendToExpenseGroup(models.Model):
    id = models.AutoField(primary_key=True)
    expense_group_id = models.ForeignKey(AddExpenseGroup, on_delete= models.CASCADE)
    invited_to_group_friend = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.expense_group_id}"



class AddExpense(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    expense_group_id = models.ForeignKey(AddExpenseGroup, on_delete= models.CASCADE)

    description = models.CharField(max_length=15, default="wydatek")
    price = models.FloatField(default= 0.0)
    repaid = models.FloatField(default= 0.0)

    
    date_added = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.description



class AddFriendToExpense(models.Model):
    id = models.AutoField(primary_key=True)
    expense_id = models.ForeignKey(AddExpense, on_delete= models.CASCADE)
    expense_group_id = models.ForeignKey(AddExpenseGroup, on_delete= models.CASCADE)
    invited_to_expense_friend = models.ForeignKey(User, on_delete=models.CASCADE)

    # proportion or amount
    amount = models.FloatField(default= 0)  
    to_repayment = models.FloatField(default= 0)  


    # def __str__(self):
    #     return f"{self.invited_to_expense_friend} hangs {AddExpense.creator} {self.amount}/{self.to_repayment} PLN. --- {self.expense_id}" 



class OpenRegistration(models.Model):
    describe = models.TextField(default="The registration is open? (Don't create new entry, edit this one)")
    is_open = models.BooleanField(default= False)



class BeerStyles(models.Model):
    id = models.AutoField(primary_key= True)
    style_name = models.TextField(default= "")
    max_carbonation = models.FloatField(default= 0)
    min_carbonation = models.FloatField(default= 0)

    class Meta:
        verbose_name = "Beer style"
        verbose_name_plural = "Beer styles"