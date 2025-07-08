from django import forms
from .models import *



class NewEventFormNew(forms.ModelForm):
    class Meta:
        model = NewEventModelNew
        fields = ['event_title', 'event_location', 'event_description', 'event_date', 'event_time']

        widgets = { 'event_title':              forms.Textarea(
                                                    attrs= {
                                                        'rows': 1, 
                                                        'style': 'resize: none;',
                                                        'placeholder': 'Tytuł wydarzenia',
                                                    }
                                                ),
                    'event_location':           forms.Textarea(
                                                    attrs= {
                                                        'rows': 1,
                                                        'style': 'resize: none;',
                                                        'placeholder': 'Lokalizacja (opcjonalnie)',
                                                    }
                                                ),
                    'event_description':        forms.Textarea(
                                                    attrs= {
                                                        'rows': 2,
                                                        'style': 'resize: none;',
                                                        'placeholder': 'Opis (opcjonalnie)',
                                                    }
                                                ),
                    'event_date':               forms.DateInput(
                                                    attrs={
                                                        'type': 'date',
                                                        'class': 'form-control',
                                                    }
                                                ),
                    'event_time':               forms.TimeInput(
                                                    attrs= {
                                                        'type': 'time',
                                                        'class': 'form-control',
                                                        'step': '60',
                                                    }
                                                ),
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