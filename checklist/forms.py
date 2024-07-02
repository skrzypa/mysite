from django import forms
from .models import Note


class TitleForm(forms.ModelForm):
    class Meta:
        model = Note

        fields = ['title']

        labels = {
            'title': 'Tytuł',
        }

        widgets = {
            'title': forms.Textarea(
                attrs= {
                    'rows': 1,
                    'class': 'form-control',
                    'placeholder': 'Tytuł',
                    'style': 'resize: none; padding: 0.5rem;'
                }
            ),
        }



class ElementForm(forms.Form):
    add_element_field = forms.CharField(
        widget= forms.Textarea(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': 'Dodaj element',
                'style': 'resize: none;'
            }
        )
    )
    


class SubgroupForm(forms.Form):
    add_subgroup_field = forms.CharField(
        widget= forms.Textarea(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': 'Dodaj podgrupę',
                'style': 'resize: none; padding: 0.5rem;'
            }
        )
    )



class SubgroupElementForm(forms.Form):
    add_subgroup_elemenet_field = forms.CharField(
        widget= forms.Textarea(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': 'Dodaj element do podgrupy',
                'style': 'resize: none; padding: 0.5rem;'
            }
        )
    )



class TextNoteForm(forms.Form):
    add_text_note_field = forms.CharField(
        widget= forms.Textarea(
            attrs= {
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Dodaj notatkę',
                'style': 'resize: none; padding: 0.5rem;'
            }
        )
    )