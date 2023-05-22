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


class NewExpenseGroupForm(forms.ModelForm):
    class Meta:
        model = AddExpenseGroup
        fields = ['expense_title']
        labels = {'expense_title': 'Tytuł'}
        widgets = {'expense_title': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),}



class NewExpenseForm(forms.ModelForm):
    class Meta:
        model = AddExpense
        fields = ['decription']
        labels = {'decription': 'Opis'}
        widgets = {'decription': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
                   'price': forms.FloatField(),}