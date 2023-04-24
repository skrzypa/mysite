from django import forms
from .models import *


class NewEventForm(forms.ModelForm):
    class Meta:
        model = NewEventModel
        fields = ['event_title', 'event_location', 'event_description', 'event_date_year', 'event_date_month', 'event_date_day']

        labels = {'event_title': 'Wydarzenie',  
                    'event_location': 'Lokalizacja', 
                    'event_description': 'Opis',
                    'event_date_year': 'Rok',
                    'event_date_month': 'Miesiąc',
                    'event_date_day': 'Dzień',
                }

        widgets = {'event_title':           forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
                   'event_location':       forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
                   'event_description':    forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
                   'event_date_year':           forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                   'event_date_month':           forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                   'event_date_day':           forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})

    # class EventTitleForm(forms.ModelForm):
    #     class Meta:
    #         model = NewEventModel
    #         fields = ['event_title']
    #         labels = {'event_title': ''}
    #         widgets = {'event_title': forms.Textarea(attrs={'cols': 50, 'rows': 1})}

    # class EventLocationForm(forms.ModelForm):
    #     class Meta:
    #         model = NewEventModel
    #         fields = ['event_location']
    #         labels = {'event_location': ''}
    #         widgets = {'event_location': forms.Textarea(attrs={'cols': 20, 'rows': 1})}

    # class EventDescriptionForm(forms.ModelForm):
    #     class Meta:
    #         model = NewEventModel
    #         fields = ['event_description']
    #         labels = {'event_description': ''}
    #         widgets = {'event_description': forms.Textarea(attrs={'cols': 100, 'rows': 2})}

    # class EventDateForm(forms.ModelForm):
    #     class Meta:
    #         model = NewEventModel
    #         fields = ['event_date']
    #         labels = {'event_date': ''}
    #         widgets = {'event_date':    forms.Textarea(attrs={'cols': 10, 'rows': 1,})}
    


class LoginForm(forms.ModelForm):
    pass