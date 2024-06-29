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
            new_record = NBP_API(currencies = data)
            new_record.save()
        
            selected_data = new_record

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


def records(request: WSGIRequest):

    return render(
        request= request,
        template_name= "currency_calc/currency_calc_records.html",
        context= {
            'records': NBP_API.objects.all()
        },
    )