from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,  logout
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import *
from .models import *

import calendar, datetime
# Create your views here.

# HOMEPAGE
def index(request):
    """Strona główna"""
            
    meetings_planner = {'name': "Meetings Planner",
                        'description': 'Aplikacja umożliwiająca tworzenie wydarzeń i zapraszanie do nich znajomych.',
                        'url': 'my_apps:meetings_calendar',
                        'images': ['meetings_1.png', 'meetings_2.png','meetings_3.png','meetings_4.png',],
                        'more_img': True,
                        }
    
    split_bills = {'name': "Split the bills",
                        'description': 'Aplikacja, dzięki której ułatwisz proces dzielenia się wydatkami z dowolną grupą ludzi.',
                        'url': 'my_apps:split_homepage',
                        'images': ['money.png',],
                        'more_img': False,
                        }
    
    beer_calculators = {'name': "Beer Calculators",
                        'description': 'Oblicz podstawowe parametry oraz sprawdź poziom nagazowania dla różnych styli piwnych.',
                        'url': 'my_apps:beer_calc',
                        'images': ['beer_1.png',],
                        'more_img': False,
                        }
    
    log_in_app = [meetings_planner, split_bills, '0']
    log_out_app = [beer_calculators, '0', '0',]

    context = {'log_in_app': log_in_app,
               'log_out_app': log_out_app,
               }

    return render(request, 'my_apps/index.html', context= context)

def contact(request):
    return render(request, 'my_apps/contact.html')
    
def admin(request):
    return render(request, 'admin')



# BEER CALC 
def calc(request):
    context, baling_wynik, brix_wynik, proc_blg_wynik, proc_bx_wynik, glukoza_wynik, roztwor_wynik = {}, 0, 0, 0, 0, 0, 0
    
    
    
    if request.method == 'POST':
        if 'brix' in request.POST:
            brix = request.POST["brix"]

            if not brix:
                context['error'] = 'Wartość wymagana'

            else:
                try:
                    brix = float(brix)
                    baling_wynik = f"{brix} Bx = {Calculators.Bx_Blg(brix)} Blg"
                except ValueError:
                    context['error'] = 'Zła wartość'



        if 'baling' in request.POST:
            baling = request.POST["baling"]

            if not baling:
                context['error'] = 'Wartość wymagana'

            else:
                try:
                    baling = float(baling)
                    brix_wynik = f"{baling} Blg = {Calculators.Blg_Bx(baling)} BX"
                except ValueError:
                    context['error'] = 'Zły typ wartości'



        if 'brix_start' in request.POST and 'brix_end' in request.POST:
            brix_s = request.POST["brix_start"]
            brix_e = request.POST["brix_end"]

            if not brix_s or not brix_e:
                context['error'] = 'Wartości wymagane'
            
            else:
                try:
                    brix_s = float(brix_s)
                    brix_e = float(brix_e)
                    proc_bx_wynik = f"Zawartość alkoholu: {brix_s} Bx → {brix_e} Bx ≈ {Calculators.Bx_proc(brix_s, brix_e)} % ± 0.5%"
                except:
                    context['error'] = 'Zły typ wartości'



        if 'blg_start' in request.POST and 'blg_end' in request.POST:
            blg_s = request.POST["blg_start"]
            blg_e = request.POST["blg_end"]

            if not blg_s or not blg_e:
                context['error'] = 'Wartości wymagane'
            
            else:
                try:
                    blg_s = float(blg_s)
                    blg_e = float(blg_e)
                    proc_blg_wynik = f"Zawartość alkoholu: {blg_s} Blg → {blg_e} Blg ≈ {Calculators.Blg_proc(blg_s, blg_e)} % ± 0.5%"
                except:
                    context['error'] = 'Zły typ wartości'



        if 'co2' in request.POST and 'piwo' in request.POST and  'temp' in request.POST:
            co2 = request.POST['co2']
            piwo = request.POST['piwo']
            temp = request.POST['temp']


            if not co2 or not piwo or not temp:
                context['error'] = 'Wartości wymagane'
            
            else:
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
            
            if not roztwor or not glukoza:
                context['error'] = 'Wartości wymagane'
            
            else:
                try:
                    roztwor = float(roztwor)
                    glukoza = float(glukoza)
                    roztwor_wynik = f"Aby uzyskać roztwór o gęstości {roztwor} Blg należ rozpuścić {glukoza} gram glukozy w {Calculators.roztwor(roztwor, glukoza)} ml wody"
                except:
                    context['error'] = 'Zły typ wartości'
            



    context = {     "baling_wynik": baling_wynik, 
                    "brix_wynik": brix_wynik, 
                    "proc_bx_wynik": proc_bx_wynik,
                    "proc_blg_wynik": proc_blg_wynik,
                    "glukoza_wynik": glukoza_wynik,
                    "roztwor_wynik": roztwor_wynik,
                    "style_piwne": Calculators.style_piwne(),
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

    # oblicz % postępy roku
    year_progress = int(datetime.datetime.now().strftime('%j')) * 100
    year_progress = year_progress / (365 + calendar.isleap(int(GenerateCalendar.year_today)))
    year_progress = round(year_progress, 1)
    
    year_choosen = request.POST.get('year_button', GenerateCalendar.year_today)  

    months_dict2 = {} # tworzymy słownik {'miesiąc': [[dni tygodnia], [dni tygodnia], ...]}
    for key, value in GenerateCalendar.months_dict.items():
        weeks = []
        for week in calendar.monthcalendar(int(year_choosen), int(value)): # 1 wersja
            days = []
            for day in week:
                if day < 10:
                    days.append(f"0{day}")
                else:
                    days.append(str(day))
            weeks.append(days)
        months_dict2[key] = weeks # 1 wersja

    # reakcje na usunięcie eventu, akceptację / odrzucenie zaproszenia
    if request.method == "POST":
        if 'delete_event' in request.POST:
            id = request.POST['delete_event']
            delete_event(request, id)
            del request.session
            return HttpResponseRedirect(reverse('my_apps:meetings_calendar'))

        elif 'accept' in request.POST:
            id = request.POST['accept']
            invited = InvitedToEventModel.objects.get(invited_friend_id= request.user.id, event_id= id)
            invited.accepted_invitation = True
            invited.decline_invitation = False
            invited.save()
            del request.session
            return HttpResponseRedirect(reverse('my_apps:meetings_calendar'))

        elif 'decline' in request.POST:
            id = request.POST['decline']
            invited = InvitedToEventModel.objects.get(invited_friend_id= request.user.id, event_id= id)
            invited.accepted_invitation = False
            invited.decline_invitation = True
            invited.save()
            del request.session
            return HttpResponseRedirect(reverse('my_apps:meetings_calendar'))
 

    # all_invited_people =    InvitedToEventModel.objects.all().filter(event__event_date_year= year_choosen)
    # all_accepted_people =   InvitedToEventModel.objects.all().filter(accepted_invitation= True).values_list('invited_friend__username', flat=True)
    # all_declined_peole =    InvitedToEventModel.objects.all().filter(decline_invitation= True).values_list('invited_friend__username', flat=True)

    all_events = []
    for event in NewEventModel.objects.all().filter(event_date_year= year_choosen).order_by('event_date_year', 'event_date_month', 'event_date_day'):
        
        # try:
        dict_all_events = {}
        dict_all_events['identifier'] = event.id
        dict_all_events['owner'] = str(event.owner)
        dict_all_events['event_title'] = event.event_title
        dict_all_events['event_location'] = event.event_location
        dict_all_events['event_description'] = event.event_description
        dict_all_events['event_date'] = f"{event.event_date_day}.{event.event_date_month}.{event.event_date_year}"
        dict_all_events['event_date_year'] = event.event_date_year
        dict_all_events['event_date_month'] = event.event_date_month
        dict_all_events['event_date_day'] = event.event_date_day

        dict_all_events['invited_friend'] = InvitedToEventModel.objects.all().filter(event__event_date_year= year_choosen, event_id = event.id).values_list('invited_friend__username', flat=True)
        dict_all_events['accepted_invitation'] = InvitedToEventModel.objects.all().filter(event__event_date_year= year_choosen, event_id = event.id, accepted_invitation= True).values_list('invited_friend__username', flat=True)
        dict_all_events['decline_invitation'] = InvitedToEventModel.objects.all().filter(event__event_date_year= year_choosen, event_id = event.id, decline_invitation= True).values_list('invited_friend__username', flat=True)
        # except UnboundLocalError:
        #     pass

        # print(str(request.user) == str(dict_all_events['invited_friend'].get())) # TRUE!
        # print(list(dict_all_events['invited_friend']))
        if request.user == event.owner or str(request.user) in list(dict_all_events['invited_friend']):
            all_events.append(dict_all_events)

    event_all_my_dates = [] # eventy utworzone przez zalogowanego użytkownika
    all_my_own_events =     NewEventModel.objects.all().filter(owner= request.user, event_date_year= year_choosen).order_by('event_date_year', 'event_date_month', 'event_date_day')
    for event in all_my_own_events:
        date = f"{event.event_date_day}.{GenerateCalendar.month_list_1[int(event.event_date_month) -1]}.{event.event_date_year}"
        event_all_my_dates.append(date)
    
    event_all_shared_dates = [] # eventy, na które zalogowany użytkonwik został zaproszony
    all_shared_event =      NewEventModel.objects.filter(invitedtoeventmodel__invited_friend= request.user, event_date_year=year_choosen).order_by('event_date_year', 'event_date_month', 'event_date_day')
    for event in all_shared_event:
        date = f"{event.event_date_day}.{GenerateCalendar.month_list_1[int(event.event_date_month) -1]}.{event.event_date_year}"
        event_all_shared_dates.append(date)


    del request.session

    
    # dane do przesłania na stronę
    context = { 'years_list':                   GenerateCalendar.years_list,     # wygenerujemy listę lat w postaci przycisków na podstawie tej listy
                'months_dict':                  GenerateCalendar.months_dict,    
                'months_dict2':                 months_dict2,    # słownik={'months_name': [[week], [week],...]}
                'days_list':                    ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sb', 'Nd'],      # lista dni pon-nd

                'day_today':                    GenerateCalendar.day_today,
                'month_today':                  GenerateCalendar.month_today,
                'month_today_2':                GenerateCalendar.month_today_2,
                'year_today':                   GenerateCalendar.year_today,
                'year_choosen':                 year_choosen,   # rok wybrany dzięki liście przycisków na stronie

                'event_all_my_dates':           event_all_my_dates,
                'event_all_shared_dates':       event_all_shared_dates,
                'current_user':                 str(request.user),
                'all_events':                   all_events,

                'year_progress':                year_progress,

                # 'all_my_own_events':            all_my_own_events,
                # 'all_my_own_events_number':     len(all_my_own_events),
                # 'all_shared_event':             all_shared_event,
                # 'all_shared_event_number':      len(all_shared_event),
                # 'all_invited_people':           all_invited_people,
                # 'all_accepted_people':          all_accepted_people,
                # 'all_declined_peole':           all_declined_peole,
            }

    return render(request= request, template_name= 'my_apps/meetings_calendar.html', context= context)

@login_required
def new_event(request):

    current_user = request.user

    observed_users_list = Friendship.objects.all().filter(from_friend= current_user)
    your_friends_list = [f.to_friend for f in observed_users_list if f.to_friend != current_user]

    if request.method != 'POST':
        # form_title = EventTitleForm()
        # form_localization = EventLocationForm()
        # form_details = EventDescriptionForm()
        day = request.GET.get('day')        # GET, bo chcemy odczytać to, nie wysłać
        month = request.GET.get('month')
        year = request.GET.get('year')

        initial_data = {'event_date_year': year,
                        'event_date_month': GenerateCalendar.months_dict[month],
                        'event_date_day': day,
                        }
        form_new_event = NewEventForm(initial= initial_data)

    else:
        form_new_event = NewEventForm(data= request.POST)
        if form_new_event.is_valid():
            new_event = form_new_event.save(commit=False)
            new_event.owner = request.user
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
                # 'form_title': form_title,
                # 'form_localization': form_localization,
                # 'form_details': form_details,
                # 'form_date': form_date,
            }
    return render(request=request, template_name='my_apps/meetings_new_event.html', context=context)

@login_required
def edit_event(request, id):

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
                        'event_date_day': event.event_date_day
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
                form_new_event.save()
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
        

            # invited_to_event = request.POST.getlist('friends')
            # # invited_to_event to lista zaznaczonych identyfikatorów zaproszonych przyjaciół
            # # możesz teraz dodać ich do modelu InvitedToEventModel
            # for friend_id in invited_to_event:
            #     invited_friend = User.objects.get(id=friend_id)
            #     print(invited_friend)
            #     if invited_friend in invited_friends:
            #         invited_model = InvitedToEventModel(event= event)
            #     else:
            #         invited_model = InvitedToEventModel(event= event, 
            #                                             invited_friend= invited_friend,
            #                                             accepted_invitation= False,
            #                                             decline_invitation= False,)
            #     invited_model.save()



    context = {'form_new_event':        form_new_event,
               'id':                    id,
               'your_friends_list':     your_friends_list,
               'invited_friends':       invited_friends,
               'rest_friends':          rest_friends,
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
            return redirect('my_apps:index')

    return render(request, "my_apps/users_log_in.html")
    
def register(request):
    """Rejestracja nowego użytkownika"""
    if request.method != 'POST':
        # Wyświetlenie pustego formularza rejestracji użytkownika
        form = UserCreationForm()

    else:
        # Przetworzenie wypełnionego formularza
        form = UserCreationForm(data= request.POST)
        if form.is_valid():
            new_user = form.save()
            # Zalogowanie użytkownika, a następnie przekierowanie do na stronę główną
            login(request, new_user)
            return redirect('my_apps:index')
    
    # Wyświetlenie pustego formularza
    context = {'form': form}
    return render(request, 'my_apps/users_register.html', context)

@login_required
def log_out(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany. Dziękuję za skorzystanie z serwisu!")
    return redirect("my_apps:index")

@login_required
def friends(request):
    current_user = request.user

    users_list = Friendship.all_users.exclude(id= current_user.id) # tworzymy listę wszystkich użytkowników (bez aktulanie zalogowanego)
    observed_users_list = Friendship.objects.all().filter(from_friend= current_user)

    followed_users = [f.to_friend for f in observed_users_list if f.to_friend != current_user]   # lista zaobserwowanych użytkowników
    # for i in followed_users:
    #     print(i)

    if request.method == 'POST':
        if 'user_to_observe_id' in request.POST:
            add_to_observed(request, current_user)
        elif 'user_to_delete_id' in request.POST:
            delete_observed_user(request, current_user)
        del request.session     # bez tej linijki odświeżanie strony powoduje wysłanie kolejengo formularza - co powoduje błędy
                                # dodatkowo dodani / usunięci znajomi pokazują się od razu, a nie po ponownym wejściu na stronę
        return HttpResponseRedirect(reverse('my_apps:users_friends'))
        



    context = { 'users_list': users_list,
                "number_of_users": len(users_list),             
                'number_of_friends': len(followed_users),    
                'followed_users': followed_users,             
                # "":,                    
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
    current_user = request.user     # print(current_user, type(request)) # skrzypa <class 'django.core.handlers.wsgi.WSGIRequest'>

    # friend_list = [friend.to_friend for friend in Friendship.objects.all().filter(from_friend= current_user)]
    # for i in friend_list:
    #     print(i)

    expense_group_list = AddExpenseGroup.objects.all()
    invited_to_group = AddFriendToExpenseGroup.objects.all()

    my_expense_group_list = []
    for group in expense_group_list.order_by("-date_added"):
        invited_to_group = invited_to_group.values_list("invited_to_group_friend__username", flat=True)
        # print(invited_to_group, group.expense_title, group.id)
        
        if current_user == group.owner or str(current_user) in invited_to_group:
            # print(group.owner, group.expense_title, group.status, group.date_added.date)
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
                expense_group.save()

                # invited_to_group = request.POST.getlist("friends")
                # print(invited_to_group)
                # for friend_id in invited_to_group:
                #     invited_friend = User.objects.get(id= friend_id)
                #     invited_model = AddFriendToExpenseGroup(expense= expense_group, 
                #                                             invited_to_group_friend= invited_friend)
                #     invited_model.save()
                return redirect(to= 'my_apps:split_group', group_id= expense_group.id)
        
        
        elif "del_group" in request.POST:
            del_group_id = request.POST["del_group"]
            # print(del_group_id)
            group_to_del = AddExpenseGroup.objects.get(id= del_group_id)
            # print(group_to_del)
            group_to_del.delete()
            return redirect(to= 'my_apps:split_homepage')

        else:
            form_add_expense_group = None

    context = {"expense_group_list": my_expense_group_list,
               "current_user": current_user,
            }

    return render(request, template_name='my_apps/split_homepage.html', context= context)


def split_group(request, group_id):
    current_user = request.user
    # print(current_user, current_user.id) # skrzypa 1
    users = User.objects
    add_friend_to_expense_group = AddFriendToExpenseGroup.objects
    add_expense_group = AddExpenseGroup.objects
    
    group_owner = add_expense_group.get(id= group_id)
    group_owner_name = str(group_owner.owner)
    group_owner_id = users.get(username= group_owner_name).id
    # print(group_owner_name, group_owner_id)

    group = add_expense_group.get(id= group_id)
    expenses = AddExpense.objects.all().filter(expense_id= group_id)
    invited_friend_to_group = add_friend_to_expense_group.all().filter(expense_id= group_id).values_list("invited_to_group_friend__username", flat= True)
    
    invited_friend_to_group_dict = {users.get(username= name).id: str(name) for name in invited_friend_to_group}
    invited_friend_to_group_dict[group_owner_id] = group_owner_name


    # sprawdzamy czy użytkownik jest właścicielem grupy lub na liście zaproszonym do niej
    if str(current_user) not in invited_friend_to_group and current_user != group.owner:
        raise Http404

    friend_list = [friend.to_friend for friend in Friendship.objects.all().filter(from_friend= current_user)]

    if request.method != "POST":
        pass

    else:
        if "invite_to_group" in request.POST: 
            invited_to_group = request.POST.getlist('friends')

            for friend_id in invited_to_group:
                # print(friend_id, User.objects.get(id= friend_id))
                # print(invited_friend_to_group)
                
                if str(User.objects.get(id= friend_id)) in invited_friend_to_group:
                    pass

                else:
                    invited_friend = users.get(id= friend_id)
                    invited_model = AddFriendToExpenseGroup(expense= group, 
                                                        invited_to_group_friend= invited_friend,
                                                    )
                    invited_model.save()
            return redirect(to= 'my_apps:split_group', group_id= group_id)
        
        if "del_friend" in request.POST:
            
            if request.user != current_user:
                # print(request.user == current_user, str(request.user) == current_user) # True, False
                raise Http404
            
            else:
                friend_to_del_id = int(request.POST["del_friend"])
                friend_to_del = add_friend_to_expense_group.get(expense_id = group_id, invited_to_group_friend= friend_to_del_id)
                # print(friend_to_del)

                friend_to_del.delete()

                return redirect(to= 'my_apps:split_group', group_id= group_id)

        elif "equal"  in request.POST:
            get_equal_list = request.POST.getlist('add_friend_to_expense')  # pobieramy id zaznaczonych użytkowników
            expense_title = str(request.POST.get('expense_title'))
            expense_price = str(request.POST.get('expense_price'))
            # print(get_equal_list, len(get_equal_list))

            equal_dict = {users.get(id= user).username: users.get(id= user).id  for user in get_equal_list}
            # print(equal_dict, len(equal_dict))

            if expense_title == "" and expense_price == "":
                messages.warning(request, "Podaj tytuł i cenę")
            elif expense_title == "":
                messages.warning(request, "Podaj tytuł")
            elif expense_price == "": 
                messages.warning(request, "Podaj cenę")
            
            else:   # zapisać aby model?
                expense_price = round(float(expense_price), 2)
                # print(expense_title, expense_price, round(expense_price / len(equal_dict), 2))
            return redirect(to= 'my_apps:split_group', group_id= group_id)




    context = {"group": group,
               "expenses": expenses,
               "friend_list": friend_list,
               "invited_friend_to_group_dict": invited_friend_to_group_dict,
               "current_user": str(current_user),
               "group_owner": group_owner_name
            }

    return render(request, template_name='my_apps/split_group.html', context= context)

