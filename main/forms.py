from django import forms
from .models import Contato

class ContatoForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cliente",
                "class": "form-control"
            }
        ))
    
    
    celular = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Celular",
                "class": "form-control"
            }
        ))
    
    mensagem = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Mensagem",
                "class": "form-control"
            }
        ))
       
    class Meta:
        model = Contato
        fields = ('nome','celular', 'mensagem')

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
