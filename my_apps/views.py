from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.core.handlers.wsgi import WSGIRequest

from .forms import *
from .models import *
from .beercalc import BeerCalc
from .meetings import Meetings
import mysite.settings

import datetime
import os
import calendar
import json
from pprint import pprint
# Create your views here.

# HOMEPAGE
def index(request: WSGIRequest):
    """Strona główna"""

    apps = AvailableApp.objects.all()
    apps_photos = AppPhotos.objects.all()

    if not os.path.exists(mysite.settings.MEDIA_ROOT):
        os.mkdir(mysite.settings.MEDIA_ROOT)


    if request.user.is_authenticated:
        new_invitations = InvitedToEventModelNew.objects.filter(
            invited_friend = User.objects.get(id = request.user.id), 
            accepted_invitation = False, 
            decline_invitation = False
        )

        if new_invitations:
            messages.warning(
                request= request,
                message= f"Masz {len(new_invitations)} nowe zaproszeni(a/e) na wydarzeni(a/e)",
                extra_tags= 'warning'
            )

    app_dict = {
        'Aplikacje dostępne po zalogowaniu:': [],
        'Aplikacje dostępne bez logowania:': [],
        'Poradniki:': [],
    }
    
    for app_nr, app in enumerate(apps, start= 1):
        if app.app_log_in is True and app.app_tutorial is False:
            key = list(app_dict.keys())[0]

        elif app.app_log_in is False and app.app_tutorial is False:
            key = list(app_dict.keys())[1]

        elif app.app_log_in is False and app.app_tutorial is True:
            key = list(app_dict.keys())[2]

        app_dict[key].append(
            {
                'app_id': app.id_app,
                'name': app.app_name,
                'description': app.app_describe,
                'url':app.app_link,
                'images': [p.photo for p in apps_photos.filter(id_app= app.id_app)],
                'more_img':  len(apps_photos.filter(id_app= app.id_app)) > 1,
                'app_log_in': app.app_log_in,
                'app_nr': app_nr,
            }
        )



    return render(
        request= request, 
        template_name= 'my_apps/homepage.html', 
        context= {
            'app_dict': app_dict,
            'app_names': [app['name'] for _, apps in app_dict.items() for app in apps]
        }
    )

def contact(request: WSGIRequest):
    return render(request, 'my_apps/contact.html')
    
def admin(request: WSGIRequest):
    return render(request, 'admin')



# BEER CALC
"""
def calc(request: WSGIRequest):
    context = {
        'style_piwne': [[i.style_name, i.min_carbonation, i.max_carbonation] for i in BeerStyles.objects.all()],
    }
    error = 'Podaj prawidłową liczbę',
    
    
    if request.method == 'POST':
        if 'brix' in request.POST:
            brix = request.POST["brix"]
            baling_result = BeerCalc().brix_to_baling(brix)

            if baling_result is None:
                context['error'] = error
            else:
                context["baling_wynik"] = f"{brix} Bx = {baling_result} Blg"
                context['url']= "bx-blg"


        elif 'baling' in request.POST:
            baling = request.POST["baling"]
            brix_result = BeerCalc().baling_to_brix(baling)

            if brix_result is None:
                context['error'] = error
            else:
                context["brix_wynik"] = f"{baling} Blg = {brix_result} Bx"
                context['url']= "bx-blg"


        elif 'brix_start' in request.POST and 'brix_end' in request.POST:
            brix_s: str = request.POST["brix_start"]
            brix_e: str = request.POST["brix_end"]

            brix_to_percent = BeerCalc().brix_to_percent(brix_s, brix_e)
            if brix_to_percent is None:
                context['error'] = error
            else:
                context["proc_bx_wynik"] = f"Zawartość alkoholu: {brix_s} Bx → {brix_e} Bx ≈ {brix_to_percent} % ± 0.5%"
                context['url']= "bx-proc"


        elif 'blg_start' in request.POST and 'blg_end' in request.POST:
            blg_s: str = request.POST["blg_start"]
            blg_e: str = request.POST["blg_end"]

            baling_to_percent = BeerCalc().baling_to_percent(blg_s, blg_e)
            if baling_to_percent is None:
                context['error'] = error
            else:
                context["proc_blg_wynik"] =  f"Zawartość alkoholu: {blg_s} Blg → {blg_e} Blg ≈ {baling_to_percent} % ± 0.5%"
                context['url']= "blg-proc"


        elif 'co2' in request.POST and 'piwo' in request.POST and  'temp' in request.POST:
            co2: str = request.POST['co2']
            piwo: str = request.POST['piwo']
            temp: str = request.POST['temp']

            glucose_for_refermentation = BeerCalc().how_much_sugar(co2, piwo, temp)
            if glucose_for_refermentation is None:
                context['error'] = error
            else:
                context["glukoza_wynik"] =  f"Aby uzyskać nagazowanie na poziomie {co2} VOL w {piwo} litrach piwa o temperaturze {temp}℃ należy dodać {glucose_for_refermentation} gram glukozy"
                context['url']= "glucose"


        elif 'blg_pocz' in request.POST and 'glukoza' in request.POST:
            roztwor: str = request.POST['blg_pocz']
            glukoza: str = request.POST['glukoza']

            sugar_solution = BeerCalc().sugar_solution(roztwor, glukoza)
            if sugar_solution is None:
                context['error'] = error
            else:
                context["roztwor_wynik"] =  f"Aby uzyskać roztwór o gęstości {roztwor} Blg należ rozpuścić {glukoza} gram glukozy w {sugar_solution} ml wody"
                context['url']= "co2-glucose"

        
    return render(request= request, 
                template_name= f'my_apps/beer_calc.html', 
                context= context,
            )
"""


# MEETINGS
class MeetingsCalendar:
    def __init__(self):
        self.date_format =                          "%Y-%m-%d %H:%M:%S"
        self.date_today: datetime.datetime =        datetime.datetime.now()
        self.formatted_date_today: str =            self.date_today.strftime(self.date_format)
        self.year_progress_proc: float =            self.year_progress()
        self.year_range: list =                     list(range(2023, self.date_today.year + 2))
        self.year_today: int =                      self.date_today.year
        self.days: list[str] =                      ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sb', 'Nd']
        self.months: list[str] =                    ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]
        self.hours: list[str] =                     [str(h).zfill(2) for h in range(0, 24)]
        self.minutes: list[str] =                   [str(m).zfill(2) for m in range(0, 60)]
        self.date_today_formatted: list[str] =      [str(self.date_today.year), str(self.months[int(self.date_today.month) - 1]), str(self.date_today.day).zfill(2)]
        
    
    def generate_calendar(self, year: int = None) -> dict:
        if year is None:
            year = self.year_today

        calendar_ = calendar.Calendar().yeardayscalendar(year, width= 1)
        formatted_calendar = {month: [] for month in self.months}

        for mnr, month in enumerate(calendar_):
            for wnr, week in enumerate(month[0]):
                w = []
                for dnr, day in enumerate(week):
                    w.append(str(calendar_[mnr][0][wnr][dnr]).zfill(2))
                formatted_calendar[list(formatted_calendar.keys())[mnr]].append(w)

        return formatted_calendar
        

    def year_progress(self) -> float:
        year_today = self.date_today.year
        past_days = int(self.date_today.strftime("%j"))
        year_progress = (past_days * 100) / (365 + calendar.isleap(year_today))
        return round(year_progress, 1)
    

    def generate_day(self, request: WSGIRequest, day: str, month: str, year_choosen: str, all_events: dict) -> str:
        events = False
        color = 'danger text-light'#'warning text-dark'
        date = False
        if not int(day) == 0:
            date = datetime.date(int(year_choosen), self.months.index(month)+1, int(day))
            events = all_events.get(str(date), False)
            
            new_invitations_this_day = InvitedToEventModelNew.objects.filter(invited_friend= request.user, accepted_invitation = False, decline_invitation = False, event__event_date = str(date))
            if new_invitations_this_day:
                color = 'warning text-dark'

        
        day_id = f"{day}.{str((self.months.index(month)+1)).zfill(2)}.{year_choosen}"

        return render(
            request= request,
            template_name= 'my_apps/meetings_day.html',
            context= {
                "day": day,
                "id": day_id,
                "today_day": 'success' if all(
                    [self.date_today_formatted[0] == year_choosen, 
                    self.date_today_formatted[1] == month, 
                    self.date_today_formatted[2] == day]
                ) else 'primary',
                "event_counter": False if not events else len(events) if len(events) > 0 else False,
                "color": color,
                "date": str(date) if date else "",
            }
        ).content.decode('utf-8')


    def generate_month(self, request: WSGIRequest, month: str, weeks: list[str], year_choosen: str, all_events: dict) -> str:
        return render(
            request= request,
            template_name= 'my_apps/meetings_month.html',
            context= {
                "month": month,
                "days": self.days,
                "weeks": [[self.generate_day(request, day, month, year_choosen, all_events) for day in week] for week in weeks],
            }
        ).content.decode('utf-8')
        

    
    def generate_full_calendar(self, request: WSGIRequest, year_choosen: int, all_events: dict) -> tuple[str]:
        calendar_choosen = self.generate_calendar(year_choosen).items()

        generate_calendar = [self.generate_month(request, month, weeks, str(year_choosen), all_events) for month, weeks in calendar_choosen]
        
        modals = []
        events = False
        for month, weeks in calendar_choosen:
            for week in weeks:
                for day in week:
                    if day != '00':
                        date = datetime.date(year_choosen, self.months.index(month)+1, int(day))
                        events = all_events.get(str(date), False)

                    day_id = f"{day}.{str((self.months.index(month)+1)).zfill(2)}.{str(year_choosen)}"
                    modals.append(
                        render(
                                request= request,
                                template_name= 'my_apps/meetings_modal_event.html',
                                context = {
                                    "id": day_id,
                                    "events": False if not events else events,
                                }
                        ).content.decode('utf-8')
                    )


        return "".join(generate_calendar), "".join(modals)
    

    def generate_event(self, request: WSGIRequest, event: NewEventModelNew, color: str) -> str:
        invited: QuerySet[InvitedToEventModelNew] = InvitedToEventModelNew.objects.filter(event= event)
        accepted: QuerySet[InvitedToEventModelNew] = invited.filter(accepted_invitation = True, decline_invitation = False)
        declined: QuerySet[InvitedToEventModelNew] = invited.filter(accepted_invitation = False, decline_invitation = True)
        
        return render(
            request,
            template_name= "my_apps/meetings_event.html",
            context = {
                'event': event,
                'color': color,
                'is_owner': event.owner == request.user,
                'id': event.id,
                "invited": invited,
                "accepted": accepted,
                "declined": declined,
            },
        ).content.decode('utf-8')
    

    def generate_events(self, request: WSGIRequest, all_events: QuerySet[NewEventModelNew]) -> tuple[dict, list]:
        generate_events = {}
        upcoming_events = []
        for e in all_events:
            e: NewEventModelNew

            time_delta = (e.event_date - self.date_today.date()).days

            if time_delta <= 7 and time_delta >= 0:
                upcoming_events.append(
                    [
                        e, 
                        'success' if time_delta==0 else 'primary'
                    ]
                )
                
            color = 'danger' if time_delta < 0 else 'success' if time_delta == 0 else 'primary'
            date = str(e.event_date)

            if date not in generate_events:
                generate_events[date] = []
            
            generate_events[date].append(self.generate_event(request, e, color))
        
        return generate_events, upcoming_events
    

    def accept_decline_invitation(self, request: WSGIRequest, event_id: str, accept: bool, decline: bool) -> JsonResponse:
        event: NewEventModelNew = NewEventModelNew.objects.get(id= event_id)

        invite: InvitedToEventModelNew = InvitedToEventModelNew.objects.get(
            event= event,
            invited_friend= User.objects.get(id= request.user.id)
        )
        invite.accepted_invitation = accept
        invite.decline_invitation = decline
        invite.save()

        time_delta = (event.event_date - self.date_today.date()).days
        update_event = self.generate_event(
            request= request, 
            event= NewEventModelNew.objects.get(id= event_id), 
            color= 'danger' if time_delta < 0 else 'success' if time_delta == 0 else 'primary'
        )

        update_counter = not InvitedToEventModelNew.objects.filter(event__event_date = str(event.event_date), accepted_invitation = False, decline_invitation = False)

        return JsonResponse(
            data= {
                'accept_decline': True,
                'event': update_event, 
                'event_id': int(event_id),
                "update_counter": update_counter,
                "day_id_to_update": f"day_{str(event.event_date)}" # yyyy-mm-dd
            }
        )


    def add_new_event(self, request: WSGIRequest) -> HttpResponseRedirect:
        form_new_event = NewEventFormNew(request.POST).save(commit= False)
        form_new_event.owner = request.user
        form_new_event.save()

        [
            InvitedToEventModelNew(
                event= form_new_event,
                invited_friend = User.objects.get(id= friend_id),
                accepted_invitation= False,
                decline_invitation= False,
                ).save() 
            for friend_id in request.POST.getlist('invited_friends')
        ]

        return redirect(to= 'my_apps:meetings_calendar')
    

    def del_add_friend_to_event(self, request: WSGIRequest, edited_event: NewEventModelNew, friends: list[User], add: bool) -> JsonResponse:
        event_id = edited_event.id

        if add:
            InvitedToEventModelNew(event= edited_event, invited_friend= User.objects.get(id= request.POST['add_friend'])).save()
        else:
            InvitedToEventModelNew.objects.get(event= edited_event, invited_friend= User.objects.get(id= request.POST['del_friend'])).delete()

        friends_in_event = [f.invited_friend for f in InvitedToEventModelNew.objects.filter(event= edited_event)]
        friends_not_in_event = [f for f in friends if f not in friends_in_event]
        return JsonResponse(
            data= {
                'success': True,
                'friend_div': render(
                    request= request, 
                    template_name='my_apps/meetings_add_del_friend_from_event.html',
                    context= {
                        'friends':                  friends, 
                        'friends_in_event':         friends_in_event,
                        'friends_not_in_event':     friends_not_in_event,
                        'event_id':                 event_id,      
                    }
                ).content.decode('utf-8')
            }
        )


        

@login_required(login_url= "my_apps:users_log_in")
def meetings_homepage(request: WSGIRequest):
    meetings = MeetingsCalendar()
    current_user = request.user
    year_choosen = request.POST.get('year_button', str(meetings.year_today))

    my_events: QuerySet[NewEventModelNew] =         NewEventModelNew.objects.filter(owner = current_user.id, event_date__year = year_choosen)
    my_invitations: QuerySet[NewEventModelNew] =    NewEventModelNew.objects.filter(invitedtoeventmodelnew__invited_friend = current_user.id, event_date__year = year_choosen)

    all_events = [e for e in my_events.union(my_invitations).order_by('-event_date', '-event_time')]
    all_events_counter = len(all_events)

    generate_events = meetings.generate_events(request, all_events)
    events, upcoming_events = generate_events[0], generate_events[1]

    if request.method == 'POST':
        if 'accept' in request.POST:
            return meetings.accept_decline_invitation(request, request.POST['accept'], True, False)

        if 'decline' in request.POST:
            return meetings.accept_decline_invitation(request, request.POST['decline'], False, True)

    if mysite.settings.DEBUG:
        print(request.POST)


    return render(
        request= request, 
        template_name= 'my_apps/meetings_calendar.html', 
        context= {
            'year_progress':        str(meetings.year_progress_proc),
            'today_date':           meetings.date_today_formatted,
            'year_range':           [str(y) for y in meetings.year_range],
            'year_choosen':         str(year_choosen),
            'year_today':           str(meetings.date_today.year),
            'calendar':             meetings.generate_full_calendar(request, int(year_choosen), events),
            'all_events_counter':   all_events_counter,
            'all_events':           events,
            'upcoming_events':      upcoming_events,
            'new_invitations':      InvitedToEventModelNew.objects.filter(invited_friend= request.user, accepted_invitation= False, decline_invitation= False)
        }
    )


@login_required(login_url= "my_apps:users_log_in")
def new_event(request: WSGIRequest, date: str):
    friends = [User.objects.get(id = f.to_friend.id) for f in Friendship.objects.filter(from_friend = request.user.id)]
    form_new_event = NewEventFormNew(
        initial= {
            'event_date': str(datetime.datetime.strptime(date, "%d.%m.%Y").date()),
            'event_time': "00:00",
        }
    )

    if request.method == "POST" and NewEventFormNew(request.POST).is_valid():
        return MeetingsCalendar().add_new_event(request)

    return render(
        request= request, 
        template_name= 'my_apps/meetings_edit_new_event.html', 
        context= {
            'title':            'Dodaj nowe wydarzenie',
            'form_event':       form_new_event,
            'edit':             False,
            'friends':          friends,
        }
    )


@login_required(login_url= "my_apps:users_log_in")
def edit_event(request: WSGIRequest, event_id: str):
    edited_event = get_object_or_404(NewEventModelNew, id= event_id)
    edited_event.event_date = str(edited_event.event_date)

    if request.user != edited_event.owner:
        raise Http404
    
    form_edit_event = NewEventFormNew(request.POST, instance= edited_event)

    friends: list[User] = [f.to_friend for f in Friendship.objects.filter(from_friend= request.user)]
    friends_in_event: list[User] = [f.invited_friend for f in InvitedToEventModelNew.objects.filter(event= edited_event)]
    friends_not_in_event: list[User] = [f for f in friends if f not in friends_in_event]

    friend_div = render(
        request= request, 
        template_name='my_apps/meetings_add_del_friend_from_event.html',
        context= {
            'friends':                  friends, 
            'friends_in_event':         friends_in_event,
            'friends_not_in_event':     friends_not_in_event,
        }
    ).content.decode('utf-8')
    

    if request.method == "POST":
        if 'edit_event' in request.POST:
            form_edit_event.save()
        
        if 'del_event' in request.POST:
            title = edited_event.event_title
            messages.error(request, message= f"Wydarzenie '{title}' zostało usunięte", extra_tags= 'danger')
            edited_event.delete()
        
        if 'del_friend' in request.POST:
            return MeetingsCalendar().del_add_friend_to_event(request, edited_event, friends, False)
        
        if 'add_friend' in request.POST:
            return MeetingsCalendar().del_add_friend_to_event(request, edited_event, friends, True)
        
        return redirect(to= 'my_apps:meetings_calendar')
    else: 
        form_edit_event = NewEventFormNew(instance= edited_event)

    return render(
        request = request,
        template_name = 'my_apps/meetings_edit_new_event.html',
        context = {
            'title':                    'Edytuj wydarzenie',
            'form_event':               form_edit_event,
            'edit':                     True,
            'event_id':                 edited_event.id,
            'friends':                  friends,
            'friends_in_event':         friends_in_event,
            'friends_not_in_event':     friends_not_in_event,
            'friend_div':               friend_div,
        },
    )


# USERS
def log_in(request: WSGIRequest):
    sites = {
        '/user_data/': 'user_data:user_data',
        '/meetings_calendar/': 'my_apps:meetings_calendar',
        '/split_the_bills/': 'split_the_bills:split_the_bills',
        '/checklist/': 'checklist:checklist',
        '/users_friends/': 'my_apps:users_friends',
    }

    if request.user.is_authenticated:
        return redirect('my_apps:homepage')

    if request.method == 'POST':
        user = authenticate(
            request,
            username= request.POST['username'],
            password= request.POST['password']
        )

        if user is not None:
            login(request, user)
            return redirect(request.POST['submit'])

    return render(request, "my_apps/users_log_in.html", {'next': sites.get(request.GET.get('next'), 'my_apps:homepage')})

 
def register(request: WSGIRequest):
    """Rejestracja nowego użytkownika"""
    context = {}

    if OpenRegistration.objects.last() is None:
        OpenRegistration().save()
    
    open_registration = OpenRegistration.objects.last().is_open
    context["open_registration"] = open_registration

    # Wyświetlenie pustego formularza rejestracji użytkownika
    if request.method != "POST":
        form = UserCreationForm()
        context['form'] = form

    if open_registration is False:
        messages.warning(
            request = request, 
            message = "Rejestracja jest zamknięta. Skontaktuj się z twórcą strony jeśli chcesz się zarejestrować",
            extra_tags = "danger",
        )

    elif open_registration is True and request.method == 'POST':
        # Przetworzenie wypełnionego formularza
        form = UserCreationForm(data= request.POST)
        if form.is_valid():
            new_user = form.save()
            # Zalogowanie użytkownika, a następnie przekierowanie do na stronę główną
            login(request, new_user)
            return redirect('my_apps:homepage')
        
        else:
            messages.error(request, "Popraw następujące błędy:", "danger")
            messages.error(request, form.errors, "danger")
        
    return render(request, 'my_apps/users_register.html', context)


@login_required(login_url= "my_apps:users_log_in")
def log_out(request: WSGIRequest):
    logout(request)
    messages.success(
        request, 
        "Zostałeś wylogowany. Dziękuję za skorzystanie ze strony!",
        "success"
    )
    return redirect("my_apps:homepage")


@login_required(login_url= "my_apps:users_log_in")
def friends(request: WSGIRequest):
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
@login_required(login_url= "my_apps:users_log_in")
def add_expense_group(request: WSGIRequest):
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