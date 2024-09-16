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

@login_required
def pagina_carrinho(request):
    """ Renderiza a pagina do carrinho, e carrega as informaçoes descritas no dict context """
    
    usuario = request.user.username

    # Obtém o usuário atual
    user = Usuario.objects.get(username=usuario)

    # Obtém o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=user).last()  # Considera apenas o primeiro carrinho, ajuste se necessário
    if not carrinho:
        return render(request, 'cart.html', {'produtos': [], 'valor_total': 0,'title':'Carrinho'})

    # Obtém os itens do carrinho
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)

    produtos_no_carrinho = [(item.produto, item.quantidade) for item in itens]

    # Calcula o valor total
    valor_total = sum(item.produto.valor * item.quantidade for item in itens)
    evento = Evento.objects.filter(usuario=user).last()

    context = {
        'carrinho': produtos_no_carrinho,  # Agora passamos os produtos com suas fotos
        'total': valor_total,
        'title':'Carrinho',
        'evento':evento,
    }
    print(valor_total)
    pag = gerar_pagamento(user,valor_total)
    print(pag)
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
