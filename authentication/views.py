from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, EventoForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView
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
        return render(request, "register.html", {"form": form,'title':'Registrar'})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            
            if get_user_model().objects.filter(username=username).exists():
                form.add_error('username', 'Este nome de usuário já está em uso.')
                return render(request, "register.html", {"form": form})
            
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
    form_class = LoginForm  # Use o formulário de login personalizado

    def get(self, request):
    
        return render(request, "login.html", {"form": self.form_class,'title':'Login'})
    
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
        form.error_messages.update(error_messages)
        
        # Chama o método pai para lidar com a renderização de um formulário inválido
        response = super().form_invalid(form)
        
        # Adiciona o erro ao contexto com base na existência do usuário
        if not user_exists:
            response.context_data['error'] = error_messages['invalid_login']
        else:
            response.context_data['error'] = error_messages['inactive']
        
        return response


class EventoView(TemplateView):
    template_name = 'evento.html'
    form_class = EventoForm

    def get(self, request):
        context = {'form':self.form_class}
        return render(request, self.template_name, context)


    def post(self, request):
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)  # Não salva no banco ainda
            evento.usuario = request.user  # Associa o usuário logado ao evento
            evento.save()  # Agora salva com o usuário
            return redirect('pagina_carrinho')  # Substitua por uma URL válida
        else:
            return render(request, "evento.html", {"form": form, "erro": form.errors})
    