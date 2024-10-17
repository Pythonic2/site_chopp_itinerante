from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, EventoForm
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from .models import Usuario, Evento
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Carrinho
from authentication.models import Usuario, Evento
from .models import ItemCarrinho
from pagamento.views import gerar_pagamento
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Produto
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging


User = Usuario
from authentication.models import Carrinho

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect("login")


class RegisterUser(CreateView):

    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {"form": form, 'title': 'Registrar'})

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
                login(request, user)  # Faz o login automático
                return redirect("cardapio")
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
        try:
            usuario = request.user.username
            user = Usuario.objects.get(username=usuario)
            evento = Evento.objects.filter(usuario=user).filter(status='Aguardando Pagamento').last()
            evento.delete()
        except:
            pass
        context = {'form':self.form_class}
        return render(request, self.template_name, context)


    def post(self, request):

        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)  # Não salva no banco ainda
            evento.usuario = request.user
            evento.status = 'Aguardando Pagamento'
            evento.save()  # Agora salva com o usuário
            return redirect('pagina_carrinho')  # Substitua por uma URL válida
        else:
            return render(request, "evento.html", {"form": form, "erro": form.errors})


method_decorator(login_required)
class PedidosView(TemplateView):
    template_name = 'sucesso.html'
    
    
    def get(self, request):
        usuario = request.user.username
        user = Usuario.objects.get(username=usuario)
        eventos = Evento.objects.filter(usuario=user).order_by('-id')
        print(f'-------------{usuario}---------')
        print(f'-------------{len(eventos)}---------')
        context = {'pagamentos':eventos}
        return render(request, self.template_name, context)




# Configurando o logger no início do arquivo
import os

logging.basicConfig(
    level=logging.DEBUG,  # Nível de log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem de log
    handlers=[logging.FileHandler('transacoes.log', mode='a'),  # Salvar no arquivo transacoes.log
              logging.StreamHandler()]  # Exibir no console também
)
@login_required
def pagina_carrinho(request):
    """ Renderiza a página do carrinho e carrega as informações descritas no dict context """
    
    usuario = request.user.username

    # Obtém o usuário atual
    user = Usuario.objects.get(username=usuario)

    # Obtém o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=user).exclude(status='pago').last()
    if not carrinho:
        return render(request, 'cart.html', {'produtos': [], 'valor_total': 0, 'title': 'Carrinho'})

    # Obtém os itens do carrinho
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)

    produtos_no_carrinho = [(item.produto, item.quantidade) for item in itens]

    # Calcula o valor total
    valor_total = sum(item.produto.valor * item.quantidade for item in itens)
    
    evento = Evento.objects.filter(usuario=user).exclude(status='pago').last()
    if evento:
        evento.carrinho = carrinho.id
        evento.valor = valor_total
        evento.save()

    context = {
        'carrinho': produtos_no_carrinho,
        'total': valor_total,
        'title': 'Carrinho',
        'evento': evento,
    }

    try:
        carrinho = carrinho.id
        evento_id = evento.id if evento else None
        pag, carrinho_id = gerar_pagamento(user.id, produtos_no_carrinho, evento_id, carrinho)
        
        context['link'] = pag
    except Exception as e:
        print(f"Erro ao gerar pagamento: {e}")
        context['link'] = '#'

    return render(request, 'cart.html', context)



def obter_quantidade_carrinho_htmx(request):
    usuario = request.user.username

    # Obtém o usuário atual
    user = Usuario.objects.get(username=usuario)

    # Obtém o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=user).last()  # Considera apenas o primeiro carrinho, ajuste se necessário
    print(carrinho)
    if not carrinho:
        return 0  # Retorna 0 se não houver carrinho

    # Obtém os itens do carrinho
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)

    # Calcula a quantidade total de todos os itens no carrinho
    quantidade_total = sum(item.quantidade for item in itens)
    
    return render(request, 'parciais/qtd_carrinho.html',{'quantidade_carrinho':quantidade_total})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        usuario = request.user.username
        print(f"Usuário autenticado: {usuario}")

        # Obtém o usuário atual
        user = Usuario.objects.get(username=usuario)
        print(user.id)

        # Tenta obter o carrinho do usuário, cria um novo se não existir
        carrinho, created = Carrinho.objects.get_or_create(usuario=user, status='Progress')

        print(f"Carrinho: {carrinho.id}, Criado agora? {created}")
        logging.info(f"Carrinho: {carrinho.id}, Criado agora? {created}")

        # Obtém o produto
        produto = get_object_or_404(Produto, pk=produto_id)
        quantidade = int(request.POST.get('quantidade', 0))

        if quantidade >= 1:
            # Verifica se o produto já está no carrinho
            item_carrinho, created = ItemCarrinho.objects.get_or_create(
                carrinho=carrinho, 
                produto=produto,
                defaults={'quantidade': quantidade}  # Define a quantidade na criação
            )

            if not created:
                # Se o produto já estiver no carrinho, atualiza a quantidade
                item_carrinho.quantidade += quantidade
                item_carrinho.save()

            # Atualiza o valor total do carrinho
            carrinho.valor += produto.valor * quantidade
            carrinho.save()

            # Mensagem de sucesso para o HTMX
            mensagem = f'''
                <span class="text-success">{quantidade} Unidade(s) do Produto "{produto.nome}" adicionado ao carrinho!</span>
                <script>removerMensagem('mensagem-produto-{produto.id}');</script>
            '''
            return HttpResponse(mensagem)

        return HttpResponse(status=400)
    
    else:
        return HttpResponse("Usuário não autenticado", status=403)


def remover_do_carrinho(request, produto_id):
    """Remove ou diminui a quantidade de um item no carrinho"""
    usuario = request.user.username
    user = get_object_or_404(Usuario, username=usuario)

    # Obtém o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=user).last()
    if not carrinho:
        return HttpResponse("Carrinho não encontrado", status=404)

    produto = get_object_or_404(Produto, pk=produto_id)
    
    # Verifica se o item existe no carrinho
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho, produto=produto).last()
    if not item_carrinho:
        return HttpResponse("Item não encontrado no carrinho", status=404)
    
    # Diminui a quantidade ou remove o item se a quantidade for menor ou igual a 1
    if item_carrinho.quantidade > 1:
        item_carrinho.quantidade -= 1
        item_carrinho.save()
    else:
        item_carrinho.delete()

    # Atualiza o valor total do carrinho
    carrinho.valor = sum(item.produto.valor * item.quantidade for item in carrinho.itens.all())
    carrinho.save()

    # Redireciona para a página do carrinho
    return HttpResponseRedirect(reverse('pagina_carrinho') + '#id_do_elemento')