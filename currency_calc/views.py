from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

import requests
import datetime
import pathlib

import mysite.settings 

# Create your views here.
def currency_calc(request):

    context = {"TEST": "TESTOWE PRZEKAZANIE CONTEXTU W REDIRECT"}

    if request.method == 'POST':
        if "download_rates" in request.POST and request.user.is_superuser:
            dowloand_currencies()
            print("Pobieram kursy") # delete it

        if "PLN_to_other" in request.POST:
            print("Przeliczam złotówki") # delete it

        if "other_to_PLN" in request.POST:
            print("Przeliczam na złotówki") # delete it

        return redirect(to= request.get_full_path(), context= context)
    
    
    return render(request, 'currency_calc/currency_calc.html', context)



def dowloand_currencies():
    dowloand_date = datetime.date.today().strftime("%d_%m_%Y")
    print(dowloand_date) # delete it

    folder_with_currencies = pathlib.Path(mysite.settings.STATICFILES_DIRS[0], "currencies")
    if not pathlib.Path.exists(folder_with_currencies):
        pathlib.Path.mkdir(folder_with_currencies)

    currencies_file = pathlib.Path(folder_with_currencies, f"{dowloand_date}_rates.txt")
    if not pathlib.Path.exists(currencies_file):
        answer_a = requests.get('http://api.nbp.pl/api/exchangerates/tables/a/')   # Tabela A kursów średnich walut obcych,
        all_currencies = answer_a.json()[0]['rates']
        number_of_currencies = len(all_currencies)


        print(currencies_file) # delete it
        print(datetime.datetime.strptime(dowloand_date, "%d_%m_%Y").date()) # delete it

        print(all_currencies, number_of_currencies) # delete it

        with open(currencies_file, 'w', encoding= "UTF-8") as file:
            for currency in all_currencies:
                file.write(f"{currency}\n")
    
    else: # read last file
        print(list(pathlib.Path.iterdir(folder_with_currencies))[::-1])