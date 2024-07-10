from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.contrib import messages
from django.http import Http404

from .models import NBP_API
from .currency_calc import CurrencyCalc, CurrencyExchangeRatesSince2002

import pprint
import datetime
import plotly.express as px


# Create your views here.
def currency_calc(request: WSGIRequest, date: str = None):
    if 'dowloand_from_link' in request.POST and request.user.is_superuser:
        link = request.POST['dowloand_from_link']
        all_dates = [c.currencies['effectiveDate'] for c in NBP_API.objects.all()]
        currencies = CurrencyExchangeRatesSince2002().records(link= link)
        for currency in currencies:
            if currency['effectiveDate'] not in all_dates:
                NBP_API(currencies = currency).save()

    user = request.user
    context = {
        'user': request.user,
        'is_superuser': request.user.is_superuser,
        'records_len': NBP_API.objects.count() if NBP_API.objects.all() else 0,
    }
    
    if not context['records_len'] and not context['is_superuser']:
        raise Http404

    if date is not None:
        try: 
            date = str(datetime.datetime.strptime(date, "%Y-%m-%d").date())
            context['record'] = NBP_API.objects.get(currencies__effectiveDate = date).currencies
        except:
            context['record'] = NBP_API.objects.last().currencies
    else:
        if not context['records_len']:
            context['record'] = {"table": "", "no": "", "effectiveDate": "", "rates": []}
        else:
            context['record'] = NBP_API.objects.last().currencies

    context['date'] = context['record']['effectiveDate']

    for currency in context['record']['rates']:
        if 'country' in currency:
            currency['currency'] = currency['country']


    if user.is_superuser:
        CC2002: CurrencyExchangeRatesSince2002 = CurrencyExchangeRatesSince2002()
        context['all_links'] = CC2002.links_list()[::-1]


    if 'PLN_to_other' in request.POST or 'other_to_PLN' in request.POST:
        CC: CurrencyCalc = CurrencyCalc()
        
        code: str = request.POST['selected_currency']
        mid: list = [c['mid'] for c in context['record']['rates'] if c['code']==code][0]

        if 'PLN_to_other' in request.POST:
            pln = request.POST['PLN_to_other'].replace(',', '.')
            amount = CC.pln_to_other(pln, mid)
            mess = f"{pln} PLN = {amount} {code}"

        elif 'other_to_PLN' in request.POST:
            other = request.POST['other_to_PLN'].replace(',', '.')
            amount = CC.other_to_pln(other, mid)
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
        context= context,
    )


def records(request: WSGIRequest):

    return render(
        request= request,
        template_name= "currency_calc/currency_calc_records.html",
        context= {
            'records': NBP_API.objects.all().order_by('-currencies__effectiveDate')
        },
    )


def sources(request: WSGIRequest):

    links = CurrencyExchangeRatesSince2002().links_list()
    dates = [" - ".join(date.split("/")[-2:]) for date in links]

    date_link = {}
    for date, link in zip(dates, links):
        date_link[date] = link
    
    dates = {}
    for record in NBP_API.objects.all()[::-1]:
        year = datetime.datetime.strptime(record.currencies['effectiveDate'], "%Y-%m-%d").year
        if year not in dates:
            dates[year] = []
        dates[year].append(record.currencies['effectiveDate'])


    return render(
        request= request,
        template_name= "currency_calc/sources.html",
        context= {
            'date_link': date_link,
            'dates': dates,
        }
    )


def plots(request: WSGIRequest):
    selected_currency = request.POST.get(
        key = 'selected_currency',
        default = 'USD'
    )

    nbp_api: NBP_API = NBP_API

    all_currencies: dict = {c['code']: c['currency'] if 'currency' in c else c['country'] for c in nbp_api.objects.last().currencies['rates']}

    records: list[dict] = []
    for record in nbp_api.objects.order_by('currencies__effectiveDate'):
        for currency in record.currencies['rates']:

            if currency['code'] == selected_currency:
                mid = currency['mid']
                code = currency['code']
                country = currency['currency'] if 'currency' in currency else currency['country']

                records.append(
                    {
                        'date': f" {record.currencies['effectiveDate']}",
                        'currency': country,
                        'code': code,
                        'mid': float(mid),
                        'hover': f" {mid} PLN",
                    }
                )
    
    start_date, end_date = records[0]['date'], records[-1]['date']
    
    plot = px.line(
        data_frame =    records,
        x =             'date',
        y =             'mid',
        hover_data =    ['hover'],
        title =         f'Średnie kursy walut dla: {selected_currency} [{all_currencies[selected_currency]}]',
        markers =       True,
        labels =        {
                            'date' : 'data ',
                            'mid': 'średni kurs ',
                            'hover': f'1 {selected_currency} '
                        },
        range_x =       [start_date, end_date],
        render_mode =   'webgl',   
        template =      'seaborn',
    ) \
    .update_layout(
        xaxis = dict(
            # rangeselector = dict(
            #     buttons = list(
            #             [
            #                 dict(count=(datetime.date.today() - datetime.date(2002, 1, 1)).days, label="all", step="day", stepmode="todate"),
            #                 dict(count=10, label="10y", step="year", stepmode="backward"),
            #                 dict(count=5, label="5y", step="year", stepmode="backward"),
            #                 dict(count=2, label="2y", step="year", stepmode="backward"),
            #                 dict(count=1, label="1y", step="year", stepmode="backward"),
            #                 dict(count=6, label="6m", step="month", stepmode="backward"),
            #                 dict(count=3, label="3m", step="month", stepmode="backward"),
            #                 dict(count=1, label="1m", step="month", stepmode="backward"),
            #             ]
            #         )
            #     ),
            rangeslider = dict(
                visible = True,
                range = [start_date, end_date],
                autorange = True,
                thickness = 0.1,
            ), 
            range = [start_date, end_date],
            type = 'date',
            #fixedrange = True, # zablokowanie możliwośc przesuwania wykresu w osi X
        )
    ).to_html()
    
    plot = f"""
    <div class="text-break word-wrap" style="min-width: 600px; min-height: 300px;">
        {plot}
    </div> 
    """

    return render(
        request= request,
        template_name= "currency_calc/plots.html",
        context= {
            'plot': plot,
            'all_currencies': all_currencies,
        }
    )