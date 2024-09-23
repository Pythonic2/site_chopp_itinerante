from django import forms
from .models import Testemunho

class FeedBackForms(forms.ModelForm):
    cliente = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome",
                "class": "form-control",
                "required": "true"
            }
        ),
    )
    tipo_evento = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Qual foi o Evento?",
                "class": "form-control",
                "required":"true",
            }
        ),
        required=False
    )
    feedback = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Comentário",
                "class": "form-control",
            }
        ),
        required=False
    )

    class Meta:
        model = Testemunho
        fields = ('cliente', 'tipo_evento', 'feedback')
