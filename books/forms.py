from django import forms
from .models import NewBook


class NewBookForm(forms.ModelForm):
    class Meta:
        model = NewBook
        fields = ['owner', 'title', 'author', 'link_to_cover', 'date', 'hide']

        labels = {
            'title': 'Tytuł książki',
            'author': 'Autor',
            'link_to_cover': 'Link do okładki',
            'date': 'Data',
            'hide': "Ukryj (inni nie będą widzieć tej książki)"
        }

        widgets = {
            'owner': forms.HiddenInput(),
            
            'title': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Wpisz tytuł',
                    'rows': 2,
                    'style': 'resize: none;'
                }
            ),

            'author': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Wpisz autora',
                    'rows': 2,
                    'style': 'resize: none;'
                }
            ),

            'link_to_cover': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'https://...',
                    'rows': 3,
                    'style': 'resize: none;'
                }
            ),

            'date': forms.DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),

            'hide': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']