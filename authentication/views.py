from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from .models import Usuario
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
User = Usuario

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect("login")




class RegisterUser(CreateView):
    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            
            # Verifica se o usuário já existe
            if get_user_model().objects.filter(username=username).exists():
                # Adiciona erro no formulário informando que o usuário já existe
                form.add_error('username', 'Este nome de usuário já está em uso.')
                return render(request, "register.html", {"form": form})
            
            # Se o usuário não existir, o cadastro continua
            form.save()
            
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                return redirect("home")
            else:
                return redirect("cardapio")
        else:
            return render(request, "register.html", {"form": form, "erro": form.errors})

    

class LoginUsuario(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        # Obtem o nome de usuário digitado no formulário
        username = form.cleaned_data.get('username')
        user_exists = User.objects.filter(username=username).exists()

        # Define mensagens de erro personalizadas
        error_messages = {
            'invalid_login': gettext_lazy('Verifique o usuário e senha e tente novamente.'),
            'inactive': gettext_lazy('Usuário inativo.'),
        }
        # Atualiza as mensagens de erro no AuthenticationForm
        AuthenticationForm.error_messages = error_messages
        
        # Chama o método pai para lidar com a renderização de um formulário inválido
        response = super().form_invalid(form)
        
        # Adiciona o erro ao contexto
        response.context_data['error'] = error_messages['invalid_login'] if not user_exists else error_messages['inactive']
        
        return response

