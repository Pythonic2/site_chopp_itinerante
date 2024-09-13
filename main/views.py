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
from .models import Usuario, Transacao, Produto
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Usuario
from django.utils.translation import gettext_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout

logger = logging.getLogger(__name__)
User = Usuario

def gerar_pagamento(cliente, valor):
    sdk = mercadopago.SDK('TEST-7847881527057924-091116-0ccb25f4e7a8318b77ae79bcb1f4c205-162016798')

    preference_data = {
        "items": [
            {
                "id": "1",
                "title": "Alguem de Chopps",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor
            }
        ],
        "external_reference": cliente,
        "back_urls": {
            "success": "http://127.0.0.1:8000/carrinho/",
            "failure": "http://127.0.0.1:8000/carrinho/",
            "pending": "http://127.0.0.1:8000/carrinho/"
        },
        "auto_return": "approved",  # Esta opção é opcional
        "notification_url": "https://webhook.site/51705b86-2cad-48f3-9228-04ed1b6c9a72"  
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
    
    carrinho = request.session.get('carrinho', {})
    total = sum(item.get('preco_total', 0) for item in carrinho.values())
    quantidade_total = sum(item.get('quantidade', 0) for item in carrinho.values())
    total = round(total, 2)
    
    # Obtendo os produtos do carrinho com suas fotos
    produtos_com_fotos = []
    for produto_id, item in carrinho.items():
        produto = Produto.objects.get(pk=produto_id)
        produto_com_foto = {
            'produto': produto,
            'valor': item['preco'],
            'quantidade': item['quantidade'],
            'preco_total': item['preco_total'],

        }
        produtos_com_fotos.append(produto_com_foto)
    
    context = {
        'carrinho': produtos_com_fotos,  # Agora passamos os produtos com suas fotos
        'total': total,
        'quantidade_carrinho': quantidade_total
    }
    # usuario = request.user.username
    # cliente = Usuario.objects.get(username=usuario)
    # valor = total
    # print(cliente.nome)
    # pag = gerar_pagamento(valor=valor, cliente=cliente.nome)
    # print(pag)
    # print(pag['init_point'])
    return render(request, 'cart.html', context)

class CardapioView(TemplateView):
    
    """ Renderiza o template do cardápio  e retona a quantidade de itens no carrinho : `quantidade_carrinho`"""
    
    template_name = 'menu.html'

    def get(self, request, **kwargs):

        context = super().get_context_data(**kwargs)
       
        context['produtos'] = Produto.objects.all()
        context['quantidade_carrinho'] = self.obter_quantidade_carrinho(request)
        return render(request, self.template_name, context)


    def obter_quantidade_carrinho(self, request):
        carrinho = request.session.get('carrinho', {})
        quantidade_total = sum(item['quantidade'] for item in carrinho.values())
        return quantidade_total


def quantidade_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    quantidade_total = sum(item['quantidade'] for item in carrinho.values())
    return render(request, 'parciais/qtd_carrinho.html',{'quantidade_carrinho':quantidade_total})


def adicionar_ao_carrinho(request, produto_id):
    """Utiliza sessão para criar o 'carrinho', e adiciona sempre que o valor do input for > 0"""
    produto = get_object_or_404(Produto, pk=produto_id)
    quantidade = int(request.POST.get('quantidade', 0))

    if quantidade >= 1:
        carrinho = request.session.get('carrinho', {})

        if produto_id in carrinho:
            carrinho[produto_id]['quantidade'] += quantidade 
            carrinho[produto_id]['preco_total'] += quantidade * float(produto.valor)
        else:
            carrinho[produto_id] = {
                'produto': produto.nome,
                'preco': float(produto.valor),
                'quantidade': quantidade,
                'preco_total': quantidade * float(produto.valor)
            }

        request.session['carrinho'] = carrinho

        # Retorna a mensagem de sucesso para o HTMX
        mensagem = f'''
            <span class="text-success">{quantidade} Unidade(s) do Produto "{produto.nome}" adicionado ao carrinho!</span>
            <script>removerMensagem('mensagem-produto-{produto.id}');</script>
        '''
        return HttpResponse(mensagem)

    # Caso a quantidade seja inválida ou não haja ação a ser tomada
    mensagem = '<span class="text-danger">Por favor, selecione uma quantidade válida para adicionar ao carrinho.</span>'
    return HttpResponse(mensagem, status=400)


def limpar_carrinho(request):
    if 'carrinho' in request.session:
        del request.session['carrinho']
        request.session.save()
    return redirect('cardapio')


def remover_do_carrinho(request, produto_id):
    print(f"Produto ID para remover: {produto_id}")
    carrinho = request.session.get('carrinho', {})
    print(f"Carrinho atual: {carrinho}")
    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]
        request.session['carrinho'] = carrinho
        request.session.save()
        print(f"Item {produto_id} removido. Novo carrinho: {carrinho}")
    else:
        print(f"Item {produto_id} não encontrado no carrinho.")
    return redirect('pagina_carrinho')


@csrf_exempt
def simple_test(request):
  
    if request.method == "POST":
        
        webhook_data = json.loads(request.body.decode('utf-8'))
        print("Webhook Recebido:", webhook_data)

        
        pagamento_id = webhook_data.get('data', {}).get('id', '')
        status = webhook_data.get('action', '')

       
        transacao = Transacao.objects.filter(transacao_id=pagamento_id).first()
        if transacao:
            transacao.status = status
            transacao.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'method_not_allowed'})


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


