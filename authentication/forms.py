from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Evento

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
        ),
        help_text="Digite a mesma senha para confirmação.",
        )
    
    class Meta:
        model = Usuario
        fields = ('nome','username', 'email', 'password1', 'password2')



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control"
            }
        ))

    class Meta:
        fields = ['username', 'password']



class EventoForm(forms.ModelForm):
    celular = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Celular",
                "class": "form-control",
                "maxlength":"11",
                "required":"true"
            }
        ),
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
    

    class Meta:
        model = Evento
        fields = ('celular', 'bairro', 'endereco', 'data_evento', 'tipo_evento')