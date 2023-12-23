from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,  logout
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.defaulttags import register

from .forms import *
from .models import *
import mysite.settings

from rubikcube.models import DescribeApp as RubikApp
from flac_mp3_tag.models import DescribeApp as FlacMp3
from deploying.models import DescribeApp as Deploying

import calendar
import datetime
import os
# Create your views here.

# HOMEPAGE
def index(request):
    """Strona główna"""

    apps = AvailableApp.objects.all()
    apps_photos = AppPhotos.objects.all()

    if not os.path.exists(mysite.settings.MEDIA_ROOT):
        os.mkdir(mysite.settings.MEDIA_ROOT)

    # [print(i.id_app, i.app_name, i.app_describe, i.app_link, i.app_log_in) for i in apps]
    # [print(i.id_app, i.id_photo, i.photo) for i in apps_photos]

    log_in_app = []
    log_out_app = []
    for app in apps:
        apps_dict = {
            'name':  app.app_name,
            'description': app.app_describe,
            'url':app.app_link,
            'images': [p.photo for p in apps_photos.filter(id_app= app.id_app)],
            'more_img':  len(apps_photos.filter(id_app= app.id_app)) > 1
        }
        # print(len(apps_photos.filter(id_app= app.id_app)) >= 1)
        # [print('/'.join(str(p.photo).split('/')[1:])) for p in apps_photos.filter(id_app= app.id_app)]
        
        if app.app_log_in is True:
            log_in_app.append(apps_dict)

        elif app.app_log_in is False:
            log_out_app.append(apps_dict)

    tutorials = [RubikApp.objects.last(), FlacMp3.objects.last(), Deploying.objects.last()]

    app_names = []
    app_names.extend([app.app_name for app in apps])
    app_names.extend([app.app_name for app in tutorials])


    context = {'log_in_app': log_in_app,
               'log_out_app': log_out_app,
               'tutorials': tutorials,
               'app_ids': app_names,
               }

    return render(request, 'my_apps/homepage.html', context= context)

def contact(request):
    return render(request, 'my_apps/contact.html')
    
def admin(request):
    return render(request, 'admin')



# BEER CALC
class BeerCalc():

    def Bx_Blg(bx):
        blg = round(bx / 1.04, 1)
        return blg

    def Blg_Bx(blg):
        bx = round(blg * 1.04, 1)
        return bx

    def Bx_proc(bx_start, bx_end): 
        blg_start = BeerCalc.Bx_Blg(bx_start)
        blg_end = BeerCalc.Bx_Blg(bx_end)
        proc_bx = BeerCalc.Blg_proc(blg_start, blg_end)
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
        return BeerStyles.objects.all()

def calc(request):
    context, baling_wynik, brix_wynik, proc_blg_wynik, proc_bx_wynik, glukoza_wynik, roztwor_wynik = {}, 0, 0, 0, 0, 0, 0
    
    
    
    if request.method == 'POST':
        if 'brix' in request.POST:
            brix = request.POST["brix"]

            try:
                brix = float(brix)
                baling_wynik = f"{brix} Bx = {BeerCalc.Bx_Blg(brix)} Blg"
            except ValueError:
                context['error'] = 'Zła wartość'



        if 'baling' in request.POST:
            baling = request.POST["baling"]

            try:
                baling = float(baling)
                brix_wynik = f"{baling} Blg = {BeerCalc.Blg_Bx(baling)} BX"
            except ValueError:
                context['error'] = 'Zły typ wartości'



        if 'brix_start' in request.POST and 'brix_end' in request.POST:
            brix_s = request.POST["brix_start"]
            brix_e = request.POST["brix_end"]

            try:
                brix_s = float(brix_s)
                brix_e = float(brix_e)
                proc_bx_wynik = f"Zawartość alkoholu: {brix_s} Bx → {brix_e} Bx ≈ {BeerCalc.Bx_proc(brix_s, brix_e)} % ± 0.5%"
            except:
                context['error'] = 'Zły typ wartości'



        if 'blg_start' in request.POST and 'blg_end' in request.POST:
            blg_s = request.POST["blg_start"]
            blg_e = request.POST["blg_end"]

            try:
                blg_s = float(blg_s)
                blg_e = float(blg_e)
                proc_blg_wynik = f"Zawartość alkoholu: {blg_s} Blg → {blg_e} Blg ≈ {BeerCalc.Blg_proc(blg_s, blg_e)} % ± 0.5%"
            except:
                context['error'] = 'Zły typ wartości'



        if 'co2' in request.POST and 'piwo' in request.POST and  'temp' in request.POST:
            co2 = request.POST['co2']
            piwo = request.POST['piwo']
            temp = request.POST['temp']

            try:
                co2 = float(co2)
                piwo = float(piwo)
                temp = float(temp)
                # glukoza_wynik = f"Aby uzyskać nagazowanie na poziomie {co2} VOL w {piwo} litrach piwa o temperaturze {temp}℃ należy dodać {Calculators.ile_glukozy(co2, piwo, temp)} gram glukozy"
                glukoza_wynik = f"Nie znalazłem jeszcze odpowiedniego wzoru :c"
            except:
                context['error'] = 'Zły typ wartości'



        if 'blg_pocz' in request.POST or 'glukoza' in request.POST:
            roztwor = request.POST['blg_pocz']
            glukoza = request.POST['glukoza']
            
            try:
                roztwor = float(roztwor)
                glukoza = float(glukoza)
                roztwor_wynik = f"Aby uzyskać roztwór o gęstości {roztwor} Blg należ rozpuścić {glukoza} gram glukozy w {BeerCalc.roztwor(roztwor, glukoza)} ml wody"
            except:
                context['error'] = 'Zły typ wartości'

    context = {     "baling_wynik": baling_wynik, 
                    "brix_wynik": brix_wynik, 
                    "proc_bx_wynik": proc_bx_wynik,
                    "proc_blg_wynik": proc_blg_wynik,
                    "glukoza_wynik": glukoza_wynik,
                    "roztwor_wynik": roztwor_wynik,
                    "style_piwne": [[i.style_name, i.min_carbonation, i.max_carbonation] for i in BeerCalc.style_piwne()],
                }

    return render(request= request, 
                    template_name= 'my_apps/beer_calc.html', 
                    context= context)



# MEETINGS
def homepage(request):
    """Strona główna"""
    return render(request, "my_apps/meetings_homepage.html")

@login_required
def calendar_generate(request):
    """Strona z kalendarzem"""

    #months
    months_dict = {'Styczeń': '01', 'Luty': '02', 'Marzec': '03', 'Kwiecień': '04', 
               'Maj': '05', 'Czerwiec': '06', 'Lipiec': '07', 'Sierpień': '08', 
               'Wrzesień': '09', 'Październik': '10', 'Listopad': '11', 'Grudzień': '12'} 

    # today date
    today = datetime.datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    today_year = today.strftime("%Y")
    today_month = today.strftime("%m")
    today_day = today.strftime("%d")
    now_hour = today.strftime("%H")
    now_minute = today.strftime(":%M")

    month_list_1 = list(months_dict.keys())     # ['Styczeń', 'Luty', ...]
    month_list_2 = list(months_dict.values())   # ['01', '02', ...]

    month_today = month_list_1[int(datetime.date.today().strftime('%m')) -1]      # np. Luty
    month_today_2 = month_list_2[int(datetime.date.today().strftime('%m')) -1]     # np. '02'



    # year progress
    year_progress = int(datetime.datetime.now().strftime('%j')) * 100
    year_progress = year_progress / (365 + calendar.isleap(int(today_year)))
    year_progress = f"{round(year_progress, 1)}"
    
    year_choosen = request.POST.get('year_button', today_year) 
    
    EventsModel = NewEventModel.objects.all()
    InvitedModel = InvitedToEventModel.objects.all() 

    months_dict2 = {} # tworzymy słownik {'miesiąc': [[dni tygodnia], [dni tygodnia], ...]}
    for key, value in months_dict.items():
        weeks = []
        for week in calendar.monthcalendar(int(year_choosen), int(value)): # 1 wersja
            days = []
            for day in week:
                days.append(str(day).zfill(2))
            weeks.append(days)
        months_dict2[key] = weeks # 1 wersja

    # reakcje na usunięcie eventu, akceptację / odrzucenie zaproszenia
    if request.method == "POST":
        if 'delete_event' in request.POST:
            id = request.POST['delete_event']
            delete_event(request, id)
            return redirect('my_apps:meetings_calendar')

        elif 'accept' in request.POST:
            id = request.POST['accept']
            invited = InvitedToEventModel.objects.get(invited_friend_id= request.user.id, event_id= id)
            invited.accepted_invitation = True
            invited.decline_invitation = False
            invited.save()
            return redirect('my_apps:meetings_calendar')

        elif 'decline' in request.POST:
            id = request.POST['decline']
            invited = InvitedToEventModel.objects.get(invited_friend_id= request.user.id, event_id= id)
            invited.accepted_invitation = False
            invited.decline_invitation = True
            invited.save()
            return redirect('my_apps:meetings_calendar')
 
    all_events = []
    for event in EventsModel.filter(event_date__year= year_choosen).order_by('event_date'):
        
        dict_all_events = {}
        dict_all_events['event'] = event

        dict_all_events['invited_friend'] = InvitedModel.filter(event_id = event.id).values_list('invited_friend__username', flat=True)
        dict_all_events['accepted_invitation'] = InvitedModel.filter(event_id = event.id, accepted_invitation= True).values_list('invited_friend__username', flat=True)
        dict_all_events['decline_invitation'] = InvitedModel.filter(event_id = event.id, decline_invitation= True).values_list('invited_friend__username', flat=True)

        if request.user == event.owner or str(request.user) in list(dict_all_events['invited_friend']):
            all_events.append(dict_all_events)

    event_all_my_dates = [] # eventy utworzone przez zalogowanego użytkownika
    all_my_own_events =     EventsModel.filter(owner= request.user, event_date_year= year_choosen).order_by('event_date_year', 'event_date_month', 'event_date_day')
    for event in all_my_own_events:
        date = f"{event.event_date_day}.{month_list_1[int(event.event_date_month) -1]}.{event.event_date_year}"
        event_all_my_dates.append(date)
    
    event_all_shared_dates = [] # eventy, na które zalogowany użytkonwik został zaproszony
    all_shared_event =      EventsModel.filter(invitedtoeventmodel__invited_friend= request.user, event_date_year=year_choosen).order_by('event_date_year', 'event_date_month', 'event_date_day')
    for event in all_shared_event:
        date = f"{event.event_date_day}.{month_list_1[int(event.event_date_month) -1]}.{event.event_date_year}"
        event_all_shared_dates.append(date)

    # dane do przesłania na stronę
    context = { 'years_list':                   [str(x) for x in range(2022, int(today_year)+2)][::-1],     # wygenerujemy listę lat w postaci przycisków na podstawie tej listy
                'months_dict':                  months_dict,    
                'months_dict2':                 months_dict2,    # słownik={'months_name': [[week], [week],...]}
                'days_list':                    ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sb', 'Nd'],      # lista dni pon-nd

                'day_today':                    str(today_day),
                'month_today':                  month_today,
                'month_today_2':                month_today_2,
                'year_today':                   str(today_year),
                'year_choosen':                 year_choosen,   # rok wybrany dzięki liście przycisków na stronie

                'event_all_my_dates':           event_all_my_dates,
                'event_all_shared_dates':       event_all_shared_dates,
                'current_user':                 request.user,
                'all_events':                   all_events,

                'year_progress':                year_progress,
            }

    return render(request= request, template_name= 'my_apps/meetings_calendar.html', context= context)

@login_required
def new_event(request):
    hours = range(0, 24)
    minutes = range(0, 60)

    current_user = request.user

    observed_users_list = Friendship.objects.all().filter(from_friend= current_user)
    your_friends_list = [f.to_friend for f in observed_users_list if f.to_friend != current_user]


    months_dict = {'Styczeń': '01', 'Luty': '02', 'Marzec': '03', 'Kwiecień': '04', 
               'Maj': '05', 'Czerwiec': '06', 'Lipiec': '07', 'Sierpień': '08', 
               'Wrzesień': '09', 'Październik': '10', 'Listopad': '11', 'Grudzień': '12'} 
    

    if request.method != 'POST':
        day = request.GET.get('day')        # GET, bo chcemy odczytać to, nie wysłać
        month = request.GET.get('month')
        year = request.GET.get('year')

        initial_data = {'event_date_year': year,
                        'event_date_month': months_dict[month],
                        'event_date_day': day,
                        }
        form_new_event = NewEventForm(initial= initial_data)

    else:
        form_new_event = NewEventForm(data= request.POST)
        if form_new_event.is_valid():
            new_event = form_new_event.save(commit=False)

            hour = request.POST['selected_hour']
            minute = request.POST['selected_minute']
            date = f"{new_event.event_date_year}-{new_event.event_date_month}-{new_event.event_date_day}"
            time = f"{hour}:{minute}"
            date_time = f"{date} {time}"

            
            new_event.owner = request.user
            new_event.event_date = date_time
            new_event.save()

            invited_to_event = request.POST.getlist('friends')
            # invited_to_event to lista zaznaczonych identyfikatorów zaproszonych przyjaciół
            # możesz teraz dodać ich do modelu InvitedToEventModel
            for friend_id in invited_to_event:
                invited_friend = User.objects.get(id=friend_id)
                invited_model = InvitedToEventModel(event= new_event, 
                                                    invited_friend= invited_friend,
                                                    accepted_invitation= False,
                                                    decline_invitation= False,
                                                )
                invited_model.save()
            

            return redirect('my_apps:meetings_calendar')

    context = {     'form_new_event': form_new_event,
                    'your_friends_list': your_friends_list,
                    'hours': hours,
                    'minutes': minutes,
            }
    return render(request=request, template_name='my_apps/meetings_new_event.html', context=context)

@login_required
def edit_event(request, id):
    hours = range(0, 24)
    minutes = range(0, 60)

    event = NewEventModel.objects.get(id= id)
    event_owner = event.owner

    if request.user != event_owner:
        raise Http404
    
    if request.method != 'POST':
        initial_data = {'event_title': event.event_title,
                        'event_location': event.event_location,
                        'event_description': event.event_description,
                        'event_date_year': event.event_date_year,
                        'event_date_month': event.event_date_month,
                        'event_date_day': event.event_date_day,
                        }
        form_new_event = NewEventForm(instance= event, initial= initial_data)

        your_friends_list = Friendship.objects.all().filter(from_friend= event_owner)
        your_friends_list  = [f.to_friend for f in your_friends_list]
        invited_friends = InvitedToEventModel.objects.all().filter(event = event)
        invited_friends = [f.invited_friend for f in invited_friends]
        rest_friends = []
        for friend in your_friends_list:
            if friend not in invited_friends:
                rest_friends.append(friend)

    else:
        form_new_event = NewEventForm(instance= event, data= request.POST)
        if 'save_event' in request.POST:
            if form_new_event.is_valid():
                edit_event = form_new_event.save(commit=False)

                hour = request.POST['selected_hour']
                minute = request.POST['selected_minute']
                date = f"{event.event_date_year}-{event.event_date_month}-{event.event_date_day}"
                time = f"{hour}:{minute}"

                edit_event.event_date = f"{date} {time}"
                edit_event.save()
                return redirect('my_apps:meetings_calendar')
        
        elif 'invite_friend_id' in request.POST:
            
            invited_friend = InvitedToEventModel(event= event, 
                                                invited_friend= User.objects.get(id= int(request.POST['invite_friend_id'])) ,
                                                accepted_invitation= False,
                                                decline_invitation= False,
                                            )
            invited_friend.save()
            return HttpResponseRedirect(reverse(f'my_apps:meetings_edit_event', args=[event.id] ))

        elif 'delete_friend_id' in request.POST:
            friend = InvitedToEventModel.objects.get(event_id= event.id, invited_friend = request.POST['delete_friend_id'])
            friend.delete()
            return HttpResponseRedirect(reverse(f'my_apps:meetings_edit_event', args=[event.id] ))



    context = {'form_new_event':        form_new_event,
                'id':                    id,
                'your_friends_list':     your_friends_list,
                'invited_friends':       invited_friends,
                'rest_friends':          rest_friends,
                'hours': hours,
                'minutes': minutes,
                'event_date_hour': event.event_date.time().hour,
                'event_date_minute': event.event_date.time().minute
                }



    return render(request= request, template_name= 'my_apps/meetings_edit_event.html', context= context)

@login_required
def delete_event(request, id):

    event = NewEventModel.objects.get(id= id)
    event_owner = event.owner

    if request.user != event_owner:
        raise Http404
    
    else:
        event.delete()
        messages.success(request, f'Wydarzenie "{event.event_title}" zostało usunięte.')



# USERS
def log_in(request):

    if request.method == 'POST':
        user = authenticate(
                        request,
                        username= request.POST['username'],
                        password= request.POST['password']
                    )

        if user is not None:
            login(request, user)
            return redirect('my_apps:homepage')

    return render(request, "my_apps/users_log_in.html")
    
def register(request):
    """Rejestracja nowego użytkownika"""

    open_registration = OpenRegistration.objects.last()
    open_registration = open_registration.is_open

    if open_registration is False:
            messages.warning(request, "Rejestracja jest zamknięta. Skontaktuj się z twórcą strony jeśli chcesz się zarejestrować")

    if request.method != 'POST':
        # Wyświetlenie pustego formularza rejestracji użytkownika
        form = UserCreationForm()

    else:
        if open_registration is True:
            # Przetworzenie wypełnionego formularza
            form = UserCreationForm(data= request.POST)
            if form.is_valid():
                new_user = form.save()
                # Zalogowanie użytkownika, a następnie przekierowanie do na stronę główną
                login(request, new_user)
                messages.success(request, "Dziękuję za założenie konta!")
                return redirect('my_apps:homepage')
        
    # Wyświetlenie pustego formularza
    context = {'form': form, 
               "open_registration": open_registration
               }
    return render(request, 'my_apps/users_register.html', context)

@login_required
def log_out(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany. Dziękuję za skorzystanie z serwisu!")
    return redirect("my_apps:homepage")

@login_required
def friends(request):
    current_user = request.user

    users_list = Friendship.all_users.exclude(id= current_user.id) # tworzymy listę wszystkich użytkowników (bez aktulanie zalogowanego)
    observed_users_list = Friendship.objects.all().filter(from_friend= current_user)

    followed_users = [f.to_friend for f in observed_users_list if f.to_friend != current_user]   # lista zaobserwowanych użytkowników

    if request.method == 'POST':
        if 'user_to_observe_id' in request.POST:
            add_to_observed(request, current_user)
        elif 'user_to_delete_id' in request.POST:
            delete_observed_user(request, current_user)
        
        return redirect('my_apps:users_friends')
        
    context = { 'users_list': users_list,
                "number_of_users": len(users_list),             
                'number_of_friends': len(followed_users),    
                'followed_users': followed_users,  
    }

    return render(request, "my_apps/users_friends.html", context= context)


def add_to_observed(request, current_user):
    added_user = request.POST['user_to_observe_id']
    friendship = Friendship(from_friend= current_user, to_friend_id= added_user)
    friendship.save()


def delete_observed_user(request, current_user):
    deleted_user = request.POST['user_to_delete_id']
    friendship = Friendship.objects.get(from_friend= current_user, to_friend_id= deleted_user)
    friendship.delete()



# SPLIT THE BILLS
@login_required
def add_expense_group(request):
    current_user = request.user 


    expense_group_list = AddExpenseGroup.objects.all().order_by("-date_added")
    invited_to_group_all = AddFriendToExpenseGroup.objects.all()

    my_expense_group_list = []
    for group in expense_group_list:
        invited_to_group = invited_to_group_all
        group_id = int(group.id)
        
        invited_to_group = invited_to_group.filter(expense_group_id= group_id).values_list("invited_to_group_friend__username", flat= True)
        
        is_owner = (current_user == group.owner)
        
        if is_owner or str(current_user) in invited_to_group:
            my_expense_group_list.append(group)

 
    if request.method != "POST":
        form_add_expense_group = NewExpenseGroupForm()
    else:
        if "create_expense_group" in request.POST:
            form_add_expense_group = NewExpenseGroupForm(data=request.POST)
            if form_add_expense_group.is_valid():
                expense_group = form_add_expense_group.save(commit=False)
                expense_group.expense_title = request.POST["expense_title"]
                expense_group.owner = current_user
                expense_group.date_added = datetime.datetime.now()
                expense_group.save()

                return redirect(to= 'my_apps:split_group', group_id= expense_group.id)
        
        
        elif "del_group" in request.POST:
            del_group_id = request.POST["del_group"]
            
            group_to_del = AddExpenseGroup.objects.get(id= del_group_id)
            
            group_to_del.delete()
            return redirect(to= 'my_apps:split_homepage')

        else:
            form_add_expense_group = None

    context = {"expense_group_list": my_expense_group_list,
               "current_user": current_user,
            }

    return render(request, template_name='my_apps/split_homepage.html', context= context)


def split_group(request, group_id):
    
    # tworzymy zmiennie wykorzystywane potem w funkcji
    current_user = request.user
    current_user_id = request.user.id
    
    users = User.objects
    add_friend_to_expense_group = AddFriendToExpenseGroup.objects
    add_expense_group = AddExpenseGroup.objects
    friendship = Friendship.objects
    add_expense = AddExpense.objects
    add_friend_to_expense = AddFriendToExpense.objects
    
    group = add_expense_group.get(id= group_id)
    group_owner_name = str(group.owner)
    group_owner_id = users.get(username= group_owner_name).id

    # wyszukujemy wydatki dla określonej grupy
    expenses = add_expense.all().filter(expense_group_id= group_id).order_by("-date_added")

    # tworzymy słownik osób zaproszonych do grupy
    invited_friend_to_group = add_friend_to_expense_group.all().filter(expense_group_id= group_id).values_list("invited_to_group_friend__username", flat= True)
    invited_friend_to_group_dict = {users.get(username= name).id: str(name) for name in invited_friend_to_group}
    invited_friend_to_group_dict[group_owner_id] = group_owner_name

    
    # sprawdzamy czy użytkownik jest właścicielem grupy lub na liście zaproszonym do niej
    if str(current_user) not in invited_friend_to_group and current_user != group.owner:
        raise Http404

    # łączymy listę wydatków oraz osób do niech zaprosznych w jeden słownik
    full_expenses = []
    for exp in expenses:
        full = {}
        full['creator'] = str(exp.creator)
        full['expense_group_id'] = exp.expense_group_id.id
        full['id'] = exp.id
        full['description'] = exp.description
        full['repaid'] = exp.repaid
        full['price'] = exp.price
        full['date_added'] = exp.date_added
        full['add_friend_to_expense'] = []
        for friend in add_friend_to_expense.filter(expense_id= exp.id):
            fr = {}
            fr['username'] = friend.invited_to_expense_friend.username
            fr['user_id'] = users.get(username= friend.invited_to_expense_friend.username).id
            fr['amount'] = friend.amount
            fr['to_repayment'] = friend.to_repayment
            full['add_friend_to_expense'].append(fr)

        full_expenses.append(full)

            

    # sprawdzamy sumę wszystkich wydatków
    sum_expenses = list(add_friend_to_expense.all().filter(expense_group_id= group_id).values_list("to_repayment", flat= True))
    sum_expenses = round(sum(sum_expenses), 2)

    sum_amount = list(add_friend_to_expense.all().filter(expense_group_id= group_id).values_list("amount", flat= True))
    sum_amount = round(sum(sum_amount), 2)

    if sum_expenses == 0.0 and len(expenses) != 0:
        status = add_expense_group.get(id= group_id)
        status.status = "Spłacona"
        status.save()
    elif len(expenses) == 0:
        status = add_expense_group.get(id= group_id)
        status.status = "Brak wydatków"
        status.save()

    # tworzymy listę osób, które są w już dodane do jakiegoś wydatku
    people_in_expense = add_friend_to_expense.filter(expense_group_id= group_id)
    people_in_expense = people_in_expense.values_list("invited_to_expense_friend__username", flat= True)
    people_in_expense = list(set(people_in_expense))
    people_in_expense = [str(users.get(username= f).username) for f in people_in_expense]

    people_in_group = add_friend_to_expense_group.filter(expense_group_id= group_id)
    people_in_group = people_in_group.values_list("invited_to_group_friend__username", flat= True)
    people_in_group = [users.get(username= f) for f in people_in_group]


    friend_list = [friend.to_friend for friend in friendship.all().filter(from_friend= current_user)]

    # tworzymy słowniki, które podsumują wszystkie wydatki w danej grupie
    all_expenses_summary = {}
    for expense in add_expense.all().filter(expense_group_id= group_id):
        creator = str(expense.creator)
        if creator not in all_expenses_summary:
            all_expenses_summary[creator] = {}

        add_friends = add_friend_to_expense.all().filter(expense_id= expense.id)
        for friend in add_friends:
            invited_friend_name = str(friend.invited_to_expense_friend)
            repayment = float(friend.to_repayment)

            if creator == invited_friend_name:
                pass
            
            elif invited_friend_name not in all_expenses_summary[creator] and repayment != 0.0:
                    all_expenses_summary[creator][invited_friend_name] = repayment

            elif invited_friend_name in all_expenses_summary[creator] and repayment != 0.0:
                    all_expenses_summary[creator][invited_friend_name] += repayment
                    all_expenses_summary[creator][invited_friend_name] = round(all_expenses_summary[creator][invited_friend_name], 2)

    if request.method != "POST":
        pass

    else:
        if "invite_to_group" in request.POST: 
            invited_to_group = request.POST.getlist('friends')

            for friend_id in invited_to_group:
                if str(users.get(id= friend_id)) in invited_friend_to_group:
                    pass

                else:
                    invited_friend = users.get(id= friend_id)
                    invited_model = AddFriendToExpenseGroup(expense_group_id= group, 
                                                        invited_to_group_friend= invited_friend,
                                                    )
                    invited_model.save()
            return redirect(to= request.get_full_path(), group_id= group_id)
        
        if "del_friend" in request.POST:
            
            if request.user != current_user:
                raise Http404
            
            
            friend_to_del_id = int(request.POST["del_friend"])
            friend_to_del = add_friend_to_expense_group.get(expense_group_id = group_id, invited_to_group_friend= friend_to_del_id)

            friend_to_del.delete()

            return redirect(to= request.get_full_path(), group_id= group_id)

        elif "equal"  in request.POST:
            get_equal_friend = request.POST.getlist('add_friend_to_expense')  # pobieramy id zaznaczonych użytkowników
            expense_title = str(request.POST.get('expense_title'))
            expense_price = request.POST.get('expense_price')

            try:
                expense_price: str = expense_price.replace(",", ".")
                expense_price = float(expense_price)
            except ValueError:
                messages.warning(request, "Zła wartość")
                return redirect(to= request.get_full_path(), group_id= group_id)

            equal_dict = {users.get(id= user).id: users.get(id= user).username for user in get_equal_friend}

            if expense_title == "" and expense_price == "":
                messages.warning(request, "Podaj tytuł i cenę")
            elif expense_title == "":
                messages.warning(request, "Podaj tytuł")
            elif expense_price == "": 
                messages.warning(request, "Podaj kwotę")
            
            else: 
                expense_group = add_expense_group.get(id= group_id)
                new_expense = AddExpense(creator = current_user,
                                        expense_group_id = expense_group,
                                        description = expense_title,
                                        price = expense_price,
                                        repaid= expense_price,
                                        date_added = datetime.datetime.now(),
                                        )
                new_expense.save()

                # dodajemy wydatek, należy więc zmienić status grupy
                expense_group.status = "Nie spłacona"
                expense_group.save()

                for user in equal_dict.items():
                    avg = round(expense_price / len(equal_dict), 2)
                    rest = round(expense_price - avg * len(equal_dict), 2)

                    user = users.get(id= user[0])

                    if current_user == user:
                        avg += rest

                    avg = round(avg, 2)
                    
                    add_friend = AddFriendToExpense(expense_id= new_expense,
                                                    expense_group_id = expense_group,
                                                    invited_to_expense_friend= user,
                                                    amount= avg,
                                                    to_repayment= avg,)
                    add_friend.save()
            return redirect(to= request.get_full_path(), group_id= group_id)

        elif "unequal" in request.POST:
            expense_title = str(request.POST.get('expense_title'))
            expense_price = request.POST.get('expense_price')
            get_unequal_friend: list = request.POST.getlist("add_friend_to_expense")  # pobieramy id zaznaczonych użytkowników
            get_unequal_amount: list = request.POST.getlist("unequal_amount")

            try:
                expense_price: str = expense_price.replace(",", ".")
                expense_price = float(expense_price)
            except ValueError:
                messages.warning(request, "Zła wartość podanej kwoty")
                return redirect(to= request.get_full_path(), group_id= group_id)
            
            try:
                get_unequal_amount = [float(amount.replace(",", ".")) for amount in get_unequal_amount]
            except ValueError:
                messages.warning(request, "Zła wartość kwoty do podziału lub nie została ona podana")
                return redirect(to= request.get_full_path(), group_id= group_id)
            
            sum_unequal = round(sum(get_unequal_amount), 2)

            if expense_title == "" and expense_price == "":
                messages.warning(request, "Podaj tytuł i kwotę")
            elif expense_title == "":
                messages.warning(request, "Podaj tytuł")
            elif expense_price == "": 
                messages.warning(request, "Podaj kwotę")
            elif sum_unequal != expense_price: 
                messages.warning(request, "Podana kwota nie równa się sumie rozdzielonych należności")

            else:
                expense_group = add_expense_group.get(id= group_id)
                new_expense = AddExpense(creator = current_user,
                                        expense_group_id = expense_group,
                                        description = expense_title,
                                        price = expense_price,
                                        repaid= expense_price,
                                        date_added = datetime.datetime.now(),
                                        )
                new_expense.save()

                #dodajemy wydatek, należy więc zmienić status grupy
                expense_group.status = "Nie spłacona"
                expense_group.save()

                for user_id, amount in zip(get_unequal_friend, get_unequal_amount):
                    user = users.get(id= user_id)

                    add_friend = AddFriendToExpense(expense_id= new_expense,
                                                    expense_group_id = expense_group,
                                                    invited_to_expense_friend= user,
                                                    amount= amount,
                                                    to_repayment= amount,)
                    add_friend.save()

            

            return redirect(to= request.get_full_path(), group_id= group_id)

        elif "edit_title" in request.POST:
            if request.user != current_user:
                raise Http404
            
            new_title = request.POST["edit_title"]
            
            save_title = add_expense_group.get(id= group_id)
            save_title.expense_title = new_title
            save_title.save()
            return redirect(to= request.get_full_path(), group_id= group_id)

        elif "to_repayment" in request.POST:
            to_repayment: str = request.POST["to_repayment"]
            to_repayment = to_repayment.split(sep=",")

            expense_to_repayment_id = to_repayment[0]
            user_to_repayment_id = to_repayment[1]
            user_to_repayment = to_repayment[2]

            # pobieramy wpisy z bazy danych
            expense_friend = add_friend_to_expense.get(expense_id_id= expense_to_repayment_id, invited_to_expense_friend= user_to_repayment_id)
            expense = add_expense.get(id= expense_to_repayment_id)

            # edytujemy wpisy w bazie danych
            expense_friend.to_repayment = 0.0
            expense_friend.save()

            expense.repaid = float(expense.repaid) - float(user_to_repayment)
            expense.save()
            
            return redirect(to= request.get_full_path(), group_id= group_id)

        elif "del_exp" in request.POST:
            exp_id = request.POST["del_exp"]
            del_exp = add_expense.get(id= exp_id)
            del_exp.delete()
            return redirect(to= request.get_full_path(), group_id= group_id)

    context = {"group": group,
               "expenses": full_expenses,
               "friend_list": friend_list,
               "invited_friend_to_group_dict": invited_friend_to_group_dict,
               "current_user": str(current_user),
               "current_user_id": current_user_id,
               "group_owner": group_owner_name,
               "sum_expenses": sum_expenses, 
               "sum_amount": sum_amount,
               "people_in_expense": people_in_expense,
               "people_in_group": people_in_group,
               "all_expenses_summary": all_expenses_summary,
            }

    return render(request, template_name='my_apps/split_group.html', context= context)


