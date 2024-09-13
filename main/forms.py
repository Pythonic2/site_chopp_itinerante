from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    celular = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Celular",
                "class": "form-control",
                "maxlength":"11",
            }
        ),
        required=False
    )
    bairro = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Bairro",
                "class": "form-control"
            }
        ),
        required=False
    )
    endereco = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Endereço",
                "class": "form-control"
            }
        ))
    data_evento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "Data do Evento",
                "class": "form-control",
                "type": "date"
            }
        ),
        required=False
    )
    tipo_evento = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tipo de Evento",
                "class": "form-control"
            }
        ),
        required=False
    )
    logo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "placeholder": "Logo",
                "class": "form-control"
            }
        ),
        required=False
    )
    cor_logo = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color'}),
        label='Cor da Logo',
        required=False,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirme a Senha",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'celular', 'bairro', 'endereco', 'data_evento', 'tipo_evento', 'logo', 'cor_logo', 'password1', 'password2')
