from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest

from .models import SplitTheBills, AddToGroup
from my_apps.models import Friendship
from mysite.settings import DATETIME_FORMAT, DATE_TIME_FORMAT

import datetime
from pprint import pprint

import plotly.express as px


# Create your views here.
class SplitTheBillsOperations:
    def __init__(self):
        ...


    def create_new_group(self, request: WSGIRequest) -> None:
        SplitTheBills(
            owner = request.user,
            title = request.POST['new_group'],
            bills = {},
            created = datetime.datetime.now(),
        ).save()
    

    def delete_group(self, request: WSGIRequest, group_id_to_delete: str) -> None:
        group_to_delete = SplitTheBills.objects.get(id = group_id_to_delete)
        if request.user == group_to_delete.owner:
            group_to_delete.delete()
            messages.error(request, message= f"Grupa '{group_to_delete.title}' została usunięta.", extra_tags= 'danger')
    

    def edit_name(self, request: WSGIRequest, group_id: str) -> None:
        group = SplitTheBills.objects.get(id = group_id)
        if request.user == group.owner:
            group.title = request.POST['edit_title']
            group.save()
    

    def add_friend_to_group(self, request: WSGIRequest, friends: list, group_id: str, added_friends: list) -> None:
        group = SplitTheBills.objects.get(id = group_id)
        friends = [User.objects.get(id = f) for f in friends]

        if request.user == group.owner:
            for f in friends:
                if f not in added_friends:
                    AddToGroup(
                        group = group,
                        added_user = f,
                    ).save()


    def del_friend_from_group(self, request: WSGIRequest, friend_to_del: str, group_id: str) -> None:
        group = SplitTheBills.objects.get(id = group_id)
        friend_to_del = User.objects.get(id = friend_to_del)

        if request.user == group.owner:
            try:
                AddToGroup.objects.get(
                    group = group, 
                    added_user = friend_to_del
                ).delete()
            except:
                ...
            else:
                messages.error(request, f"Usunięto '{friend_to_del.username}' z '{group.title}'.", extra_tags='danger')
    

    def add_equal(self, request: WSGIRequest, group_id: str, data: dict) -> None:
        group = SplitTheBills.objects.get(id = group_id)
        users = [User.objects.get(id = user_id) for user_id in data['invited_to_expense']]
        data['invited_to_expense'] = [[user.id, user.username] for user in users]
        
        try:
            data['expense_price'] = float(data['expense_price'])
        except ValueError:
            data['expense_price'] = float(0)



        if data['expense_price'] <= 0:
            messages.error(request, "Kwota musi być większa niż 0!", "danger")
        
        elif not data['title']:
            messages.error(request, "Podaj tytuł!", "danger")
        
        else:
            len_users = len(users)
            equal = round(data['expense_price'] / len_users, 2)

            if equal * len_users != data['expense_price']:
                diff = round(data['expense_price'] - equal * len_users, 2)
            else:
                diff = 0

            for user in data['invited_to_expense']:
                user.append(equal)
                user.append(equal)
                if request.user.username == user[1]:
                    user[2] += diff; user[2] = round(user[2], 2)
                    user[3] += diff; user[3] = round(user[3], 2)

            group.bills['bills'].append(data)
            group.save()


    def del_bill(self, request: WSGIRequest, bill_index: str, group_id: str) -> None:
        bill_index = int(bill_index)
        group = SplitTheBills.objects.get(id = group_id)

        del group.bills['bills'][bill_index]

        group.save()
    

    def pay_off_bill(self, request: WSGIRequest, bill_index: str, group_id: str) -> None:
        bill_index = [int(i) for i in bill_index.split(sep= '.')]
        group = SplitTheBills.objects.get(id = group_id)

        group.bills['bills'][bill_index[0]]['invited_to_expense'][bill_index[1]][3] = 0

        group.save()
    

    def make_summary(self, group_id: str) -> None:
        group = SplitTheBills.objects.get(id = group_id)

        # add three new keys
        group.bills['summary']['amount_to_repay'] = 0
        group.bills['summary']['amount_repaid'] = 0
        group.bills['summary']['summary_table'] = None
        group.save()


        try:
            expenses = [expense['invited_to_expense'] for expense in group.bills['bills']]
        except KeyError:
            return None

        # change of status if everything has been paid
        repaid = []
        for bill in group.bills['bills']:
            for user in bill['invited_to_expense']:
                repaid.append(user[3] == 0)

        repaid = all(repaid)

        if repaid:
            group.status = True
        
        if group.status is True and not repaid:
            group.status = False


        # add up the amounts
        for users in expenses:
            for user in users:
                group.bills['summary']['amount_to_repay'] += user[2]
                group.bills['summary']['amount_repaid'] += user[3]

        group.bills['summary']['amount_diff'] = round(group.bills['summary']['amount_to_repay'] - group.bills['summary']['amount_repaid'], 2)
        group.bills['summary']['amount_to_repay'] = round(group.bills['summary']['amount_to_repay'], 2)
        group.bills['summary']['amount_repaid'] = round(group.bills['summary']['amount_repaid'], 2)


        group.bills['summary']['summary_table'] = self._summary_table(group_id)


        group.save()


    def _user_does_not_exist(self) -> bool: ...
    

    def make_pie_chart(self, group_id: str) -> str | None:
        group = SplitTheBills.objects.get(id = group_id)

        try:
            group.bills['summary']
        except KeyError:
            return None
        

        if 'amount_to_repay' in group.bills['summary'] and 'amount_repaid' in group.bills['summary']:

            return px.pie(
                data_frame= {
                    'Legenda': ['Kwota do spłaty', 'Spłacona kwota'],
                    'Wartość': [
                        round(group.bills['summary']['amount_to_repay'] - group.bills['summary']['amount_diff'], 2), 
                        group.bills['summary']['amount_diff'],
                    ],
                },
                names='Legenda',
                values='Wartość'
            ).to_html()
        
        return None


    def _summary_table(self, group_id: str) -> dict | None:
        group = SplitTheBills.objects.get(id = group_id)
        bills = [bill for bill in group.bills['bills']]

        if not bills:
            return None 
        

        bills_summary = {}

        for bill in bills:
            for user in bill['invited_to_expense']:
                creator = bill['creator']

                if creator not in bills_summary:
                    bills_summary[creator] = {}

                if user[1] != creator:

                    if user[1] not in list(bills_summary[creator].keys()):
                        bills_summary[creator][user[1]] = [0, 0]
                          
                    if user[1] in list(bills_summary[creator].keys()):
                        bills_summary[creator][user[1]][0] += user[2]
                        bills_summary[creator][user[1]][1] += user[3]

                        bills_summary[creator][user[1]][0] = round(bills_summary[creator][user[1]][0], 2)
                        bills_summary[creator][user[1]][1] = round(bills_summary[creator][user[1]][1], 2)
                
        return bills_summary
    

    def pay_off_the_entire_bill(self, request: WSGIRequest, group_id: str, bill_idx: str):
        group = SplitTheBills.objects.get(id = group_id)
        users = group.bills['bills'][int(bill_idx)]['invited_to_expense']

        for idx, _ in enumerate(users):
            users[idx][-1] = 0.0

        group.save()


    def mark_again_for_repayment(self, request: WSGIRequest, group_id: str, bill_idx: str):
        group = SplitTheBills.objects.get(id = group_id)
        users = group.bills['bills'][int(bill_idx)]['invited_to_expense']

        for idx, _ in enumerate(users):
            users[idx][-1] = users[idx][-2]

        group.save()

    
    def add_unequal(self, request: WSGIRequest, group_id: str, expense_title: str, expense_price: str, add_people_to_expense: list, unequal_amount: list):
        group = SplitTheBills.objects.get(id = group_id)

        for idx, u in enumerate(unequal_amount):
            if u == '':
                unequal_amount[idx] = 0
            else:
                unequal_amount[idx] = float(u)
    
        expense_price = round(sum(unequal_amount), 2)
        users = [User.objects.get(id = f) for f in add_people_to_expense]
        bills = group.bills['bills']


        if any([u <= 0 for u in unequal_amount]):
            messages.error(request, "Kwota musi być większa niż 0!", "danger")
        
        elif not expense_title:
            messages.error(request, "Podaj tytuł!", "danger")
        
        else:
            new_bill = {
                'title': expense_title,
                'creator': request.user.username,
                'expense_price': expense_price,
                'invited_to_expense': [[user.id, user.username, amount, amount] for user, amount in zip(users, unequal_amount)],
                'time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            }
            bills.append(new_bill)
            group.save()

            

@login_required(login_url= "my_apps:users_log_in")
def split_the_bills(request: WSGIRequest):
    stb: SplitTheBillsOperations = SplitTheBillsOperations()

    if request.method == 'POST':
        if 'new_group' in request.POST:
            stb.create_new_group(request)
        elif 'del_group':
            stb.delete_group(request, request.POST['del_group'])



    return render(request= request, template_name= "split_the_bills/split_the_bills.html", 
        context= {
            'all_groups': SplitTheBills.objects.filter(owner = request.user)\
                .union(
                    SplitTheBills.objects.filter(addtogroup__added_user = request.user)
                )\
                .order_by('-created'),
            'user': request.user,
        }
    )


@login_required(login_url= "my_apps:users_log_in")
def split_the_bills_group(request: WSGIRequest, group_id: str):
    group: SplitTheBills = SplitTheBills.objects.get(id = group_id)
    stb: SplitTheBillsOperations = SplitTheBillsOperations()
    friends = [User.objects.get(id = f.to_friend.id) for f in Friendship.objects.filter(from_friend = request.user)]
    added_friends = [User.objects.get(id = f.added_user.id) for f in AddToGroup.objects.filter(group = group_id)]

    if request.user not in added_friends and request.user != group.owner:
        raise Http404
    
    pie_chart = stb.make_pie_chart(group_id)

    if request.user == group.owner:
        added_friends.insert(0, request.user)
    else:
        added_friends.insert(0, group.owner)

    
    if group.bills == {}:
        group.bills = {"bills": [], "summary": {}}
        group.save()

    if request.method == "POST":
        if 'edit_title' in request.POST:
            stb.edit_name(request, group_id)

        if 'friends' in request.POST:
            stb.add_friend_to_group(request, request.POST.getlist('friends'), group_id, added_friends)

        if 'del_friend' in request.POST:
            stb.del_friend_from_group(request, request.POST['del_friend'], group_id)

        if 'equal' in request.POST:
            stb.add_equal(request, group_id, 
                data = {
                    'title': request.POST['expense_title'],
                    'creator': request.user.username,
                    'expense_price': request.POST['expense_price'],
                    'invited_to_expense': request.POST.getlist('add_people_to_expense'),
                    'time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                }
            )

        if 'del_bill' in request.POST:
            stb.del_bill(request, request.POST['del_bill'], group_id)

        if 'pay_off_bill' in request.POST:
            stb.pay_off_bill(request, request.POST['pay_off_bill'], group_id)

        if 'pay_off_the_entire_bill' in request.POST:
            stb.pay_off_the_entire_bill(request, group_id, request.POST['pay_off_the_entire_bill'])
        
        if 'mark_again_for_repayment' in request.POST:
            stb.mark_again_for_repayment(request, group_id, request.POST['mark_again_for_repayment'])

        if 'unequal' in request.POST:
            stb.add_unequal(request, group_id, request.POST['expense_title'], request.POST['expense_price'], request.POST.getlist('add_people_to_expense'), request.POST.getlist('unequal_amount'))

        stb.make_summary(group_id)
        
        return redirect(to= "split_the_bills:split_the_bills_group", group_id= group_id)


    stb.make_summary(group_id)


    return render(request= request, template_name= "split_the_bills/split_the_bills_group.html", 
        context= {
            'user': request.user,
            'group': group,
            'friends': friends,
            'added_friends': added_friends,
            'pie_chart': pie_chart,
            'amount_to_repay': group.bills['summary'].get('amount_to_repay', 0),
            'amount_repaid': group.bills['summary'].get('amount_repaid', 0),
            'amount_diff': group.bills['summary'].get('amount_diff', 0),
            'summary_table': group.bills['summary'].get('summary_table', None)
        }
    )