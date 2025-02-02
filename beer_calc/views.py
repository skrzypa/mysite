from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse


from .forms import BrixToBlgForm, BlgToBrixForm, BrixToAlcoholForm, BalingToAlcoholForm, CarbonationOfBeerForm, SearchForm
from .beer_calc import BeerCalc
from .models import BeerStyles, ButtonIcon

import json

# Create your views here.
def beer_calc(request: WSGIRequest):
    
    BC = BeerCalc()

    if request.method == 'POST':

        if request.content_type == 'application/json':
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
        else:
            body = request.POST


        form_brix = BrixToBlgForm(body)
        if form_brix.is_valid():
            brix_value = form_brix.cleaned_data['brix_to_blg_field']
            blg_value = BC.brix_to_baling(brix_value)
            return JsonResponse({'success': True, 'blg': blg_value}, status=200)
        

        form_baling = BlgToBrixForm(body)
        if form_baling.is_valid():
            baling_value = form_baling.cleaned_data['baling_to_brix_field']
            brix_value = BC.baling_to_brix(baling_value)
            return JsonResponse({'success': True, 'brix': brix_value}, status=200)
        

        form_brix_alc = BrixToAlcoholForm(body)
        if form_brix_alc.is_valid():
            start_end = form_brix_alc.cleaned_data['brix_start_field'], form_brix_alc.cleaned_data['brix_end_field']
            if start_end[0] < start_end[1]:
                return JsonResponse({'success': False, 'error': 'Brixy początkowe nie mogą być większe od brixów końcowych'}, status=200)
            alcohol = BC.brix_to_percent(start_end[0], start_end[1])
            return JsonResponse({'success': True, 'alcohol': alcohol}, status=200)
        

        form_baling_alc = BalingToAlcoholForm(body)
        if form_baling_alc.is_valid():
            start_end = form_baling_alc.cleaned_data['baling_start_field'], form_baling_alc.cleaned_data['baling_end_field']
            if start_end[0] < start_end[1]:
                return JsonResponse({'success': False, 'error': 'Balingi początkowe nie mogą być większe od balingów końcowych'}, status=200)
            alcohol = BC.baling_to_percent(start_end[0], start_end[1])
            return JsonResponse({'success': True, 'alcohol': alcohol}, status=200)
        

        form_carbonation = CarbonationOfBeerForm(body)
        if form_carbonation.is_valid():
            co2 = form_carbonation.cleaned_data['co2_field']
            temperature = form_carbonation.cleaned_data['temperature_field']
            volume = form_carbonation.cleaned_data['beer_volume_field']
            blg_start = form_carbonation.cleaned_data['blg_start_field']
           
            glucose = BC.how_much_sugar(co2, volume, temperature)
            glucose_solution = BC.sugar_solution(blg_start, glucose)
            return JsonResponse({'success': True, 'glucose': glucose, 'glucose_solution': glucose_solution}, status=200)

    return render(
        request,
        'beer_calc/beer_calc.html',
        context = {
            'brix_to_blg': BrixToBlgForm(),
            'baling_to_brix': BlgToBrixForm(),
            'brix_alc': BrixToAlcoholForm(),
            'baling_alc': BalingToAlcoholForm(),
            'carbonation': CarbonationOfBeerForm(),

            'div_style': "max-width: 500px; background-color: rgb(255, 255, 255); margin: 1rem; padding: 15px; border-radius: 20px; width: 100vh;",

            'div_table_style': "max-width: 750px; background-color: rgb(255, 255, 255); margin: 1rem; padding: 15px; border-radius: 20px; width: 100vh;",

            'title_div': 'word-wrap text-break text-center text-dark mb-3',

            'beer_styles': [[nr, beer.style_name, beer.min_carbonation, beer.max_carbonation] for nr, beer in enumerate(BeerStyles.objects.all(), start= 1)],

            'icon': ButtonIcon.objects.last().photo.url,

            'search_form': SearchForm(),

            'site_name': 'PS | BeerCalc'
        }
    )