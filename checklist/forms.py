from django import forms
from .models import Note


class NewNoteForm(forms.Form):

    new_note_field = forms.CharField(
        help_text= "Podaj tytuł nowej notatki",
        widget = forms.TextInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',
            }
        )
    )



class ChangeTitleForm(forms.Form):

    change_title_field = forms.CharField(
        label = 'gsdgsdgsd',
        widget = forms.TextInput(
            attrs= {
                'label': "gsdgsdgsd",
                'rows': 1,
                'class': 'form-control text-break word-wrap text-light h1 text-center',
                'placeholder': '',
                'style': 'resize: none; background-color: rgba(0,0,0,0); margin-top: 1rem; border: 2px solid;',
            }
        )
    )



class NewElementForm(forms.Form):

    type_of_element_field = forms.ChoiceField(
        help_text = "Wybierz rodzaj notatki do dodania:",
        choices = (
            ('', '---- Wybierz ----'), 
            ('1', 'Notatka tekstowa'), 
            ('2', 'Element'), 
            # ('3', 'Grupa')
        ),
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
    )

    element_field = forms.CharField(
        help_text = "Treść elementu:",
        widget = forms.TextInput(
            attrs= {
                'rows': 1,
                'class': 'form-control',
                'placeholder': '',
                'style': 'resize: none;',
            }
        )
    )



class ChangeTextForm(forms.Form):

    change_text_field = forms.CharField(
        widget= forms.Textarea(
            attrs= {
                'rows': '5',
                'class': 'form-control text-break word-wrap text-light',
                'placeholder': '',
                'style': 'background-color: rgba(0,0,0,0); margin-top: 1rem; border: 2px solid white; font-size: 15px;',
                "readonly": "readonly",
            }
        )
    )


    def __init__(self, *args, **kwargs):
        auto_id = kwargs.pop("auto_id", None)
        super().__init__(*args, **kwargs)
        if auto_id:
            self.fields["change_text_field"].widget.attrs["id"] = auto_id



class ChangeElementForm(forms.Form):

    change_element_field = forms.CharField(
        widget= forms.TextInput(
            attrs= {
                'class': 'form-control text-break word-wrap text-light',
                'placeholder': '',
                'style': 'background-color: rgba(0,0,0,0); margin-top: 1rem; border: 2px solid white; font-size: 13px; height: 40px',
                "readonly": "readonly",
            }
        )
    )


    def __init__(self, *args, **kwargs):
        auto_id = kwargs.pop("auto_id", None)
        super().__init__(*args, **kwargs)
        if auto_id:
            self.fields["change_element_field"].widget.attrs["id"] = auto_id



class ChangeGroupForm(forms.Form):

    change_group_field = forms.CharField(
        widget= forms.TextInput(
            attrs= {
                'class': 'form-control text-break word-wrap text-light',
                'placeholder': '',
                'style': 'background-color: rgba(0,0,0,0); margin-top: 1rem; border: 2px solid white; font-size: 13px; height: 40px',
                "readonly": "readonly",
            }
        )
    )


    def __init__(self, *args, **kwargs):
        auto_id = kwargs.pop("auto_id", None)
        super().__init__(*args, **kwargs)
        if auto_id:
            self.fields["change_group_field"].widget.attrs["id"] = auto_id



"""
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

"""