from django import forms


class BrixToBlgForm(forms.Form):
    brix_to_blg_field = forms.FloatField(
        help_text= 'Brix',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.01,
                'min': 0,
                'max': 30,
            }
        ),
    )



class BlgToBrixForm(forms.Form):
    baling_to_brix_field = forms.FloatField(
        help_text= 'Baling',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.01,
                'min': 0,
                'max': 30,
            }
        ),
    )



class BrixToAlcoholForm(forms.Form):
    brix_start_field = forms.FloatField(
        help_text= 'Brix początkowe',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.01,
                'min': 0,
                'max': 30,
            }
        )
    )

    brix_end_field = forms.FloatField(
        help_text= 'Brix końcowe',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.01,
                'min': 0,
                'max': 30,
            }
        )
    )



class BalingToAlcoholForm(forms.Form):
    baling_start_field = forms.FloatField(
        help_text= 'Baling początkowe',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.01,
                'min': 0,
                'max': 30,
            }
        )
    )

    baling_end_field = forms.FloatField(
        help_text= 'Baling końcowe',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.01,
                'min': 0,
                'max': 30,
            }
        )
    )



class CarbonationOfBeerForm(forms.Form):
    co2_field = forms.FloatField(
        help_text= 'Poziom CO2',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.01,
                'min': 2.0,
                'max': 3.5,
            }
        )
    )

    temperature_field = forms.FloatField(
        help_text= 'Temperatura piwa [°C]',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.1,
                'min': 0,
                'max': 30,
            }
        )
    )
    
    beer_volume_field = forms.FloatField(
        help_text= 'Objętość piwa [L]',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.1,
                'min': 0,
                'max': 25,
            }
        )
    )
    
    blg_start_field = forms.FloatField(
        help_text= 'Baling początkowe',
        widget= forms.NumberInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',

                'step': 0.1,
                'min': 0,
                'max': 30,
            }
        )
    )