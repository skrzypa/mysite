from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import QuerySet

from django.core.handlers.wsgi import WSGIRequest

from .forms import *
from .models import *
from .beercalc import BeerCalc
from .meetings import Meetings
import mysite.settings

import datetime
import os
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



# MEETINGS
@login_required
def meetings_homepage(request: WSGIRequest):
    meetings = Meetings()
    current_user = request.user
    current_user_id = current_user.id
    year_choosen = request.POST.get('year_button', str(meetings.year_today))

    my_events: QuerySet[NewEventModelNew] =         NewEventModelNew.objects.filter(owner = current_user_id, event_date__year = year_choosen)
    my_invitations: QuerySet[NewEventModelNew] =    NewEventModelNew.objects.filter(invitedtoeventmodelnew__invited_friend = current_user_id, event_date__year = year_choosen)

    all_events = my_events.union(my_invitations).order_by('event_date', 'event_time')
    all_events_counter = len(all_events)


    if request.method == 'POST':

        for m in messages.get_messages(request):
            del m

        if 'accept_invitation' in request.POST:
            invitation = InvitedToEventModelNew.objects.get(
                event = NewEventModelNew.objects.get(id = request.POST['accept_invitation']),
                invited_friend = User.objects.get(id = current_user_id)
            )
            invitation.accepted_invitation = True
            invitation.decline_invitation = False
            invitation.save()

            return redirect(to= 'my_apps:meetings_calendar')

        elif 'decline_invitation' in request.POST:
            invitation = InvitedToEventModelNew.objects.get(
                event = NewEventModelNew.objects.get(id = request.POST['decline_invitation']),
                invited_friend = User.objects.get(id = current_user_id)
            )
            invitation.accepted_invitation = False
            invitation.decline_invitation = True
            invitation.save()

            return redirect(to= 'my_apps:meetings_calendar')


    events = {}
    past_future_events: dict[str, list] = {'Przyszłe wydarzenia': [], 'Przeszłe wydarzenia': [],}
    for event in all_events:
        event: NewEventModelNew
        key = f"{str(event.event_date.year)}-{meetings.months[event.event_date.month - 1]}-{str(event.event_date.day).zfill(2)}"

        invited = [User.objects.get(id = f.invited_friend.id) for f in InvitedToEventModelNew.objects.filter(event = event)]
        accepted_the_invitation = [User.objects.get(id = f.invited_friend.id) for f in InvitedToEventModelNew.objects.filter(event = event, accepted_invitation = True, decline_invitation = False)]
        not_accept_the_invitation = [User.objects.get(id = f.invited_friend.id) for f in InvitedToEventModelNew.objects.filter(event = event, accepted_invitation = False, decline_invitation = True)]

        new_invitations = InvitedToEventModelNew.objects.filter(
            event = event, invited_friend = User.objects.get(id = current_user_id), accepted_invitation = False, decline_invitation = False
        )

        if key not in events:
            events[key] = {
                'event': [[event, invited, accepted_the_invitation, not_accept_the_invitation]],
                'count': 1,
                'color': 'warning' if new_invitations else 'danger',
            }
        else:
            events[key]['event'].append([event, invited, accepted_the_invitation, not_accept_the_invitation])
            events[key]['count'] += 1
        
        if (event.event_date - meetings.date_today.date()).days < 0:
            past_future_events['Przeszłe wydarzenia'].append([event, 'danger'])
        else:
            past_future_events['Przyszłe wydarzenia'].append([event, 'success'])

        if new_invitations:  
            messages.warning(
                request= request,
                message= f"Masz nowe zaproszenie w dniu: {' '.join(key.split('-')[::-1])}",
                extra_tags= 'warning',
            )
        
        if (event.event_date - meetings.date_today.date()).days in list(range(0, 7)):
            messages.info(
                request= request,
                message= f"Nadciągające wydarzenie: \"{event.event_title}\" - {' '.join(key.split('-')[::-1])}",
                extra_tags= 'info'
            )


    return render(
        request= request, 
        template_name= 'my_apps/meetings_calendar.html', 
        context= {
            'year_progress':        str(meetings.year_progress),
            'year_choosen':         str(year_choosen),
            'year_range':           [str(y) for y in meetings.year_range],
            'year_today':           str(meetings.date_today.year),

            'today_date':           [str(meetings.date_today.year), str(meetings.months[int(meetings.date_today.month) - 1]), str(meetings.date_today.day).zfill(2)],

            'calendar':             meetings.generate_calendar(int(year_choosen)),
            'days':                 meetings.days,
            'events':               events,
            'current_user':         current_user,
            'current_user_id':      current_user_id,
            'past_future_events':   past_future_events,
            'all_events_counter':   all_events_counter,
        }
    )


@login_required
def new_event(request: WSGIRequest, year: str):
    form_new_event = NewEventFormNew()
    meetings = Meetings()
    meetings.generate_calendar(int(year))

    friends = [User.objects.get(id = f.to_friend.id) for f in Friendship.objects.filter(from_friend = request.user.id)]

    if request.method == "POST":
        if 'new_event' in request.POST:
            new_event: NewEventModelNew = form_new_event.save(commit= False)
            new_event.owner =              User.objects.get(id = request.user.id)
            new_event.event_title =        request.POST['event_title'] 
            new_event.event_location =     request.POST['event_location']
            new_event.event_description =  request.POST['event_description'] 
            new_event.event_date =         '-'.join((request.POST['event_date'].split('-')[::-1]))
            new_event.event_time =         ':'.join([request.POST['selected_hour'], request.POST['selected_minute']])

            if new_event.event_date == "" or new_event.event_time == "":
                messages.warning(
                    request = request, 
                    message= "Należy podać datę oraz godzinę", 
                    extra_tags= "danger"
                )
                return HttpResponseRedirect(reverse(viewname= 'my_apps:meetings_new_event', args=[year]))

            else:
                new_event.save()

                for friend in request.POST.getlist('friends'):
                    invited_to_event: InvitedToEventModelNew = InvitedToEventModelNew(
                        event = new_event,
                        invited_friend = User.objects.get(id = friend),
                        accepted_invitation= False,
                        decline_invitation= False,
                    )
                    invited_to_event.save()

            return redirect(to= 'my_apps:meetings_calendar')

    return render(
        request= request, 
        template_name= 'my_apps/meetings_new_event.html', 
        context= {
            'form_new_event':       form_new_event,
            'year':                 str(year),
            'calendar':             meetings.generate_calendar(int(year)),
            'hours':                meetings.hours,
            'minutes':              meetings.minutes,
            'friends':              friends,
            'days':                 meetings.days,
            'year_range':           meetings.year_range,
            'today_date':           [str(meetings.date_today.year), str(meetings.months[int(meetings.date_today.month) - 1]), str(meetings.date_today.day).zfill(2)],
        }
    )


@login_required
def edit_event(request: WSGIRequest, id):
    edited_event: NewEventModelNew = NewEventModelNew.objects.get(id = id)

    if request.user != edited_event.owner:
        raise Http404
    
    meetings = Meetings()
    invited = [f.invited_friend for f in InvitedToEventModelNew.objects.filter(event = edited_event)]
    rest_friends = [f.to_friend for f in Friendship.objects.filter(from_friend = request.user) if f.to_friend not in invited]
    
    if request.method != "POST":
        form_new_event: NewEventFormNew = NewEventFormNew(initial = {
            'event_title':          edited_event.event_title,  
            'event_location':       edited_event.event_location, 
            'event_description':    edited_event.event_description,
            'event_date':           "-".join([str(d).zfill(2) for d in [edited_event.event_date.day, edited_event.event_date.month, edited_event.event_date.year]]),
            'event_time':           [str(t).zfill(2) for t in [edited_event.event_time.hour, edited_event.event_time.minute]],
        })

    else:
        if 'save_changes' in request.POST and request.user == edited_event.owner:
            edited_event.event_title =          request.POST['event_title']
            edited_event.event_location =       request.POST['event_location']
            edited_event.event_description =    request.POST['event_description']
            edited_event.event_date =           '-'.join(request.POST['event_date'].split('-')[::-1])
            edited_event.event_time =           f"{request.POST['selected_hour']}:{request.POST['selected_minute']}"
            edited_event.save()

            for friend in request.POST.getlist('del_friends'): 
                InvitedToEventModelNew.objects.get(
                    event = edited_event, 
                    invited_friend = User.objects.get(id = friend)
                ).delete()

            for friend in request.POST.getlist('add_friends'): 
                InvitedToEventModelNew(
                    event = edited_event, 
                    invited_friend = User.objects.get(id = friend)
                ).save()

            return HttpResponseRedirect(reverse(viewname= 'my_apps:meetings_edit_event', args= [id]))
        
        elif 'del_event' in request.POST and request.user == edited_event.owner:
            edited_event.delete()
            messages.error(
                request= request,
                message= f"Usunięto wydarzenie: {edited_event.event_title}",
                extra_tags= "danger"
            )
            return redirect(to= 'my_apps:meetings_calendar')
        
        else:
            raise Http404

        


    return render(
        request = request,
        template_name = 'my_apps/meetings_edit_event.html',
        context = {
            'form_new_event':       form_new_event,
            'year':                 str(edited_event.event_date.year),
            'calendar':             meetings.generate_calendar(int(edited_event.event_date.year)),
            'hours':                meetings.hours,
            'minutes':              meetings.minutes,
            'friends':              '',
            'event_time':           [str(t).zfill(2) for t in [edited_event.event_time.hour, edited_event.event_time.minute]],
            'invited_friends':      invited,
            'rest_friends':         rest_friends,
            'days':                 meetings.days,
            'today_date':           [str(meetings.date_today.year), str(meetings.months[int(meetings.date_today.month) - 1]), str(meetings.date_today.day).zfill(2)],
        },
    )


# USERS
def log_in(request: WSGIRequest):

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
            return redirect('my_apps:homepage')

    return render(request, "my_apps/users_log_in.html")

 
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


@login_required
def log_out(request: WSGIRequest):
    logout(request)
    messages.success(
        request, 
        "Zostałeś wylogowany. Dziękuję za skorzystanie ze strony!",
        "success"
    )
    return redirect("my_apps:homepage")


@login_required(login_url= "")
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
@login_required
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