from django.shortcuts import render, redirect
import mercadopago
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Usuario, Produto, Transacao  # Certifique-se de importar seus modelos
import json
import logging
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Usuario, Transacao, Produto, Carrinho, ItemCarrinho
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Usuario
from django.utils.translation import gettext_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.views.generic import TemplateView
from .models import Produto, Carrinho, ItemCarrinho, Usuario

logger = logging.getLogger(__name__)
User = Usuario

def gerar_pagamento(cliente, valor):
    sdk = mercadopago.SDK('TEST-7847881527057924-091116-0ccb25f4e7a8318b77ae79bcb1f4c205-162016798')
    valor_float = float(valor)

    preference_data = {
        "items": [
            {
                "id": "1",
                "title": "Alguem de Chopps",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor_float
            }
        ],
        "external_reference": f'{cliente}',
        "back_urls": {
            "success": "http://127.0.0.1:8000/carrinho/",
            "failure": "http://127.0.0.1:8000/carrinho/",
            "pending": "http://127.0.0.1:8000/carrinho/"
        },
        "auto_return": "approved",  # Esta opção é opcional
        "notification_url": "https://choppitinerante.cloudboosterlab.org/pag/"  
    }

    result = sdk.preference().create(preference_data)
    preference = result['response']

    return preference

def home(request):
    produtos = Produto.objects.filter(disponivel=True)
    return render(request, 'index.html', {'produtos': produtos})

@login_required
def pagina_carrinho(request):
    """ Renderiza a pagina do carrinho, e carrega as informaçoes descritas no dict context """
    
    usuario = request.user.username

    # Obtém o usuário atual
    user = Usuario.objects.get(username=usuario)

    # Obtém o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=user).first()  # Considera apenas o primeiro carrinho, ajuste se necessário
    if not carrinho:
        return render(request, 'cart.html', {'produtos': [], 'valor_total': 0})

    # Obtém os itens do carrinho
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)

    produtos_no_carrinho = [(item.produto, item.quantidade) for item in itens]

    # Calcula o valor total
    valor_total = sum(item.produto.valor * item.quantidade for item in itens)
    
    context = {
        'carrinho': produtos_no_carrinho,  # Agora passamos os produtos com suas fotos
        'total': valor_total,
    }
    print(valor_total)
    pag = gerar_pagamento(user.username, valor_total)
    print(pag)
    return render(request, 'cart.html', context)


class CardapioView(TemplateView):
    """Renderiza o template do cardápio e retorna a quantidade de itens no carrinho"""
    
    template_name = 'menu.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['produtos'] = Produto.objects.all()
        usuario = request.user.username
        
        # Obtém o usuário atual
        user = get_object_or_404(Usuario, username=usuario)
        
        # Obtém o carrinho do usuário ou cria um novo se não existir
        carrinho, created = Carrinho.objects.get_or_create(usuario=user)
        
        # Se o carrinho foi criado, inicialize o valor
        if created:
            carrinho.valor = 0
            carrinho.save()

        # Obtém os itens do carrinho
        itens = ItemCarrinho.objects.filter(carrinho=carrinho)
        
        # Calcula a quantidade total de todos os itens no carrinho
        quantidade_total = sum(item.quantidade for item in itens)
        context['quantidade_carrinho'] = quantidade_total
        
        return render(request, self.template_name, context)


def obter_quantidade_carrinho_htmx(request):
    usuario = request.user.username

    # Obtém o usuário atual
    user = Usuario.objects.get(username=usuario)

    # Obtém o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=user).first()  # Considera apenas o primeiro carrinho, ajuste se necessário
    print(carrinho)
    if not carrinho:
        return 0  # Retorna 0 se não houver carrinho

    # Obtém os itens do carrinho
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)

    # Calcula a quantidade total de todos os itens no carrinho
    quantidade_total = sum(item.quantidade for item in itens)
    
    return render(request, 'parciais/qtd_carrinho.html',{'quantidade_carrinho':quantidade_total})


def adicionar_ao_carrinho(request, produto_id):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        usuario = request.user.username
        print(f"Usuário autenticado: {usuario}")

        # Obtém o usuário atual
        user = Usuario.objects.get(username=usuario)

        # Tenta obter o carrinho do usuário, cria um novo se não existir
        carrinho, created = Carrinho.objects.get_or_create(usuario=user)

        print(f"Carrinho: {carrinho}, Criado agora? {created}")
        
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
    carrinho = Carrinho.objects.filter(usuario=user).first()
    if not carrinho:
        return HttpResponse("Carrinho não encontrado", status=404)

    produto = get_object_or_404(Produto, pk=produto_id)
    
    # Verifica se o item existe no carrinho
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()
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
    return redirect('pagina_carrinho')


@csrf_exempt
def simple_test(request):
    if request.method == "POST":
        try:
            # Carregar dados do webhook
            webhook_data = json.loads(request.body.decode('utf-8'))
            print("Webhook Recebido:", webhook_data)
            
            pagamento_id = webhook_data.get('data', {}).get('id', '')
            status = webhook_data.get('action', '')
            external_reference = webhook_data.get('data', {}).get('external_reference', '')

            # Atualizar status da transação
            transacao = Transacao.objects.filter(transacao_id=pagamento_id).first()
            if transacao:
                transacao.status = status
                transacao.save()
                
                # Verificar se a external_reference corresponde a um pedido ou usuário
                try:
                    pedido = Pedido.objects.get(id=external_reference)
                    pedido.status = status  # Atualizar status do pedido com base no pagamento
                    pedido.save()

                    # Notifique o usuário ou tome outras ações necessárias
                    usuario = Usuario.objects.get(id=pedido.usuario.id)
                    # Exemplo: Enviar um e-mail para o usuário notificando sobre o pagamento
                    # send_payment_notification_email(usuario, pedido)

                except Pedido.DoesNotExist:
                    print(f"Pedido com ID {external_reference} não encontrado")

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Erro ao processar dados'}, status=400)
    else:
        return JsonResponse({'status': 'method_not_allowed'}, status=405)

def listar_transacoes(request):
    transacoes = Transacao.objects.all()
    return render(request, 'transacoes.html', {'transacoes': transacoes})


def logout_view(request):
    logout(request)
    return redirect("login")


class RegisterUser(TemplateView):
    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('okkkkkkk')
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                # Autentica o usuário e redireciona para o painel de controle
                return redirect("home")
            else:
                # Se o usuário não for autenticado, pode ser uma questão de integridade do banco de dados
                return redirect("cardapio")
        else:
            # Se o formulário não for válido, retorna o formulário com uma mensagem de erro
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


