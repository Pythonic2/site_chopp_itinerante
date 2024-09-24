from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Carrinho
from authentication.models import Usuario, Evento
from carrinho.models import ItemCarrinho
from pagamento.views import gerar_pagamento
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from produto.models import Produto
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging

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

