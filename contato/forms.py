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

