from django.db import models

from django.contrib.auth.models import User, AbstractUser # powiążemy wpis z danym użytkownikiem


import datetime
import calendar


# Create your models here.
class Calculators():

    def Bx_Blg(bx):
        blg = round(bx / 1.04, 1)
        return blg

    def Blg_Bx(blg):
        bx = round(blg * 1.04, 1)
        return bx

    def Bx_proc(bx_start, bx_end): 
        blg_start = Calculators.Bx_Blg(bx_start)
        blg_end = Calculators.Bx_Blg(bx_end)
        proc_bx = Calculators.Blg_proc(blg_start, blg_end)
        return proc_bx

    def Blg_proc(blg_start, blg_end): 
        proc_blg = round((blg_start - blg_end) / 1.938, 1)
        return proc_blg
    
    def ile_glukozy(co2, piwo, temp):
        # glukoza = (co2 * piwo) / (0.8115 + (0.0125 * temp))
        glukoza = (piwo * co2 * (temp / 20)) / (0.811 * 1000 * co2)
        glukoza = round(glukoza, 2)
        return glukoza
    
    def roztwor(bx_pocz, glukoza):
        woda_ml = round(glukoza * 100 / bx_pocz, 2)
        return woda_ml

    def style_piwne():
        grodziskie = {
                    'Styl': 'Grodziskie', 
                    'Nagazowanie minimalne.': 2.5, 
                    'Nagazowanie maksymalne': 3.1
                    }

        porter = {
                    'Styl': 'Porter', 
                    'Nagazowanie minimalne': 2.3, 
                    'Nagazowanie maksymalne': 2.9
                    }

        ipa = {
                    'Styl': 'India Pale Ale',  
                    'Nagazowanie minimalne': 2.4,  
                    'Nagazowanie maksymalne': 2.9
                    }

        stout = {
                    'Styl': 'Stout',  
                    'Nagazowanie minimalne': 2.4,  
                    'Nagazowanie maksymalne': 3.0
                    }

        witbier = {
                    'Styl': 'Witbier',  
                    'Nagazowanie minimalne': 2.6,  
                    'Nagazowanie maksymalne': 3.4
                    }

        hefeweizen = {
                    'Styl': 'Hefeweizen',  
                    'Nagazowanie minimalne': 2.2,  
                    'Nagazowanie maksymalne': 2.8
                    }

        style_piwne = [grodziskie, porter, ipa, stout, witbier, hefeweizen]
        
        return style_piwne

        # for piwo in style_piwne:                            # iteracja przez listę
        #     for key, value in piwo.items():                 # iteracja przez k i v słownika 
        #         print(f"{key} \033[96m{value}\033[0m")      # wyświetlenie k i v słownika



class NewEventModel(models.Model):
    """ Wydarzenie tworzone przez użytkownika """
    owner = models.ForeignKey(User, on_delete= models.CASCADE) # powiążemy wpis z danym użytkownikiem

    event_title = models.CharField(max_length= 20, default= "")
    event_location = models.CharField(max_length= 20, default= "")
    event_description = models.CharField(max_length= 200, default= "")
    event_date_year = models.CharField(max_length= 4, default= "")
    event_date_month = models.CharField(max_length= 2, default= "")
    event_date_day = models.CharField(max_length= 2, default= "")

    date_added = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        """ Zwraca reprezentację modelu w postaci ciągu tekstowego """
        return self.event_title



class InvitedToEventModel(models.Model):
    event = models.ForeignKey(NewEventModel, on_delete=models.CASCADE)
    invited_friend = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted_invitation = models.BooleanField(default= False) # 1 - przyjął; 0 - brak odp./odrzucił
    decline_invitation = models.BooleanField(default= False) # 1 - odrzucił; 0 - brak odp./przyjął



class GenerateCalendar():
    months_dict = {'Styczeń': '01', 'Luty': '02', 'Marzec': '03', 'Kwiecień': '04', 
               'Maj': '05', 'Czerwiec': '06', 'Lipiec': '07', 'Sierpień': '08', 
               'Wrzesień': '09', 'Październik': '10', 'Listopad': '11', 'Grudzień': '12'} 

    month_list_1 = list(months_dict.keys())     # ['Styczeń', 'Luty', ...]
    month_list_2 = list(months_dict.values())   # ['01', '02', ...]

    day_today = datetime.date.today().strftime('%d')
    # month_today = datetime.date.today().strftime('%m')
    month_today = month_list_1[int(datetime.date.today().strftime('%m')) -1]      # xD zadziałało np. Luty
    month_today_2 = month_list_2[int(datetime.date.today().strftime('%m')) -1]     # np. '02'
    year_today = datetime.date.today().strftime('%Y')
    
    years_list = [str(x) for x in range(2022, int(year_today)+2)]
    years_list = years_list[::-1]


    # słowniczek

    # ForeignKey czyli klucz zewnętrzny
    # klucz zewnętrzny to pojęcie z terminologii stosowanej w bazach danych, które oznacza odwołanie do innego rekordu w bazie danych
    # tutaj łączym lokalizację i szczegóły z danym wydarzeniem
    # kiedy Django musi utworzyć połączenie między dwoma fragmentami danych, wówczas wykorzystuje powiązane z nimi klucze
    # połączenie będziemy wkrótce stosować do pobierania wszystkich lokalizacji i szczegółów z powiązanym wydarzeniem

    # __str__ nakazuje które informacje



class Friendship(models.Model):
    from_friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'from_friends')
    to_friend = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'friends')

    all_users = User.objects.all()

    class Meta:
        # Dzięki temu ograniczeniu, nie będzie można dodać do bazy danych dwóch obiektów "Friendship" 
        # z tymi samymi wartościami pól "from_friend" i "to_friend
        unique_together = ('from_friend', 'to_friend')  

    def __str__(self):
        return f"{self.from_friend} add {self.to_friend} to friend"
    
# class LoginModel():
#     pass

# class RegisterModel():
#     pass


# class ProfilePhoto(AbstractUser):
#     # blank - opcjonalne pole, null - pole może mieć wartość null w bazie danych
#     profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)   

