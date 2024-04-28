from django import forms
from .models import *



class NewEventFormNew(forms.ModelForm):
    class Meta:
        model = NewEventModelNew
        fields = ['event_title', 'event_location', 'event_description', 'event_date', 'event_time']

        labels = {  'event_title':          'Tytuł',  
                    'event_location':       'Lokalizacja (opcjonalnie)', 
                    'event_description':    'Opis (opcjonalnie)',
                    'event_date':           'Data',
                    'event_time':           'Godzina',
        }

        widgets = { 'event_title':              forms.Textarea(attrs= {'rows': 1, 'class': 'h1'}),
                    'event_location':           forms.Textarea(attrs= {'rows': 1}),
                    'event_description':        forms.Textarea(attrs= {'rows': 3}),
                    'event_date':               forms.DateInput(attrs= {'readonly': 'readonly'}),
                    'event_time':               forms.TimeInput(attrs= {'readonly': 'readonly'}),
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
        fields = ['description']
        labels = {'description': 'Opis'}
        widgets = {'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
                   'price': forms.FloatField(),}