from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.contrib import messages

import requests
import datetime
import pathlib
import ast
import re
import os

import mysite.settings 
from .models import NBP_API
from .currency_calc import CurrencyCalc

# Create your views here.
folder_with_currencies = pathlib.Path(mysite.settings.MEDIA_ROOT, "currencies")


def currency_calc(request, parametr_result= None, parametr_message= None):

    if not os.path.exists(folder_with_currencies):
        os.mkdir(folder_with_currencies)

    try:
        date_and_currencies = read_currencies()
    except IndexError:
        dowloand_currencies()
    finally:
        date_and_currencies = read_currencies()
        
    data_date = date_and_currencies[0]
    currencies = date_and_currencies[1:]

    context = {
            "data_date": data_date,
            "currencies": currencies,
            "nr_of_currencies": len(currencies),
            'result': parametr_result,
            'message': parametr_message,
            'input_value1': '',
            'input_value2': '',
            'currency_choose': 'EUR'
            }  
    
    if parametr_result is not None:
        context['result'] = parametr_result

    if parametr_message is not None:
        context['message'] = parametr_message


    if request.method == 'POST':
        if "download_rates" in request.POST and request.user.is_superuser:
            dowloand_currencies()
            return redirect(to= request.get_full_path())

        # Przeliczanie PLN na inną walutę
        if "PLN_to_other" in request.POST:
            selected_currency = request.POST['selected_currency']

            for currency in currencies:
                if currency['code'] == selected_currency:
                    code = currency['code']
                    currency_name = currency['currency']
                    mid = float(currency['mid'])

            try:
                pln: str = request.POST["PLN"]
                if ',' in pln:
                    pln = pln.replace(',', '.')
                pln = float(pln)
                context['input_value1'] = pln
            except ValueError:
                result = False
                message = "Podaj prawidłową kwotę"
            else:
                result = True
                message = f"{pln} PLN = {round(pln / mid, 2)} {code}"

            return redirect(
                            reverse(
                                viewname= "currency_calc:currency_calc_with_params", 
                                args=[result, message]
                                ))

        # Przeliczanie innych walut na PLN
        if "other_to_PLN" in request.POST:
            selected_currency = request.POST['selected_currency']

            for currency in currencies:
                if currency['code'] == selected_currency:
                    code = currency['code']
                    currency_name = currency['currency']
                    mid = float(currency['mid'])

            try:
                other: str = request.POST["Other"]
                if ',' in other:
                    other = other.replace(',', '.')
                other = float(other)
                context['input_value2'] = other
            except ValueError:
                result = False
                message = "Podaj prawidłową kwotę"
            else:
                result = True
                message = f"{other} {code} = {round(other * mid, 2)} PLN"

            return redirect(
                            reverse(
                                viewname= "currency_calc:currency_calc_with_params", 
                                args=[result, message]
                                ))

        context['result'] = result
        context['currency_choose'] = code
        context['message'] = message
    
    return render(request, 'currency_calc/currency_calc.html', context)



def dowloand_currencies():
    """ Download exchange rates from the NBP API and delete oldest rates """
    if os.path.exists(folder_with_currencies):
        for file in pathlib.Path.iterdir(folder_with_currencies):
            os.remove(str(file))

    format = "%Y_%m_%d"
    dowloand_date = datetime.date.today().strftime(format)

    currencies_file = pathlib.Path(folder_with_currencies, f"{dowloand_date}_rates.txt")
    if not pathlib.Path.exists(currencies_file):
        answer_a = requests.get('http://api.nbp.pl/api/exchangerates/tables/a/')   # Tabela A kursów średnich walut obcych,
        all_currencies = answer_a.json()[0]['rates']
        number_of_currencies = len(all_currencies)

        with open(currencies_file, 'w', encoding= "UTF-8") as file:
            for currency in all_currencies:
                file.write(f"{currency}\n")


def read_currencies() -> list:   
    """ Load the latest exchange rates from the NBP API """
    files = list(pathlib.Path.iterdir(folder_with_currencies))


    last_file_date = str(files[0]).split("\\")[-1]
    last_file_date = re.findall("[0-9]+", last_file_date)
    last_file_date = "_".join(last_file_date)
    last_file_date = datetime.datetime.strptime(last_file_date, "%Y_%m_%d").date()

    date_and_currencies = [last_file_date,]
    with open(str(files[0]), 'r', encoding= "UTF-8") as file:
        for line in file.readlines():
            line = ast.literal_eval(line)   # converting str to dict
            date_and_currencies.append(line) 

    return date_and_currencies

""" NEW """
def currency_calc_new(request: WSGIRequest):

    records: QuerySet = NBP_API.objects.all().order_by('-currencies__effectiveDate')
    if not records:
        NBP_API(currencies = CurrencyCalc().currencies).save()
    
    
    selected_data: NBP_API = NBP_API.objects.get(
        id = request.POST.get(
            key= 'select_data', 
            default= NBP_API.objects.last().id
        )
    )


    # only admin can dowloand new rates
    if (request.user.is_superuser) and ('download_rates' in request.POST):
        data = CurrencyCalc().currencies
        data_date = data['effectiveDate']

        # save data if not in db
        if not data_date in [r.currencies['effectiveDate'] for r in records]:
            NBP_API(currencies = data).save()
        

    if 'PLN_to_other' in request.POST or 'other_to_PLN' in request.POST: 
        selected_currency = request.POST['selected_currency']
        currency: dict = [c for c in selected_data.currencies['rates'] if c['code'] == selected_currency][0]
        mid: float = float(currency['mid'])
        code: str = currency['code']

        if 'PLN_to_other' in request.POST:
            pln = request.POST['PLN'].replace(',', '.')
            amount = CurrencyCalc().pln_to_other(pln, mid)
            mess = f"{pln} PLN = {amount} {code}"

        elif 'other_to_PLN' in request.POST:
            other = request.POST['Other'].replace(',', '.')
            amount = CurrencyCalc().other_to_pln(other, mid)
            mess = f"{other} {code} = {amount} PLN"
        

        if amount is None:
            messages.warning(
                request= request,
                message= "Podaj prawidłową wartość",
                extra_tags= 'danger'
            )

        else:
            messages.success(
                request= request,
                message= mess,
                extra_tags= 'success'
            )


    return render(
        request= request,
        template_name= 'currency_calc/currency_calc_new.html',
        context= {
            'records': records,
            'selected_data': selected_data,
        }
    )