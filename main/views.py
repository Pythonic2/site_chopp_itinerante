from django.shortcuts import render, redirect
import mercadopago
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Cliente, Produto, Transacao  # Certifique-se de importar seus modelos
import json
import logging

# Configuração de logging
logger = logging.getLogger(__name__)
def home(request):
    """
    Página inicial.
    """
    # Listar todos os produtos disponíveis
    produtos = Produto.objects.filter(disponivel=True)

    # Renderiza a página com os produtos disponíveis e um formulário para seleção
    return render(request, 'index.html', {'produtos': produtos})


@csrf_exempt
def create_payment_link(request):
    """
    View para criar um link de pagamento para vários produtos selecionados.
    """
    if request.method == 'POST':
        try:
            # Obtém os produtos do carrinho a partir do corpo da solicitação
            data = json.loads(request.body)
            cart = data.get('cart', [])
            
            if not cart:
                logger.error("Carrinho está vazio.")
                return JsonResponse({"error": "Carrinho vazio."}, status=400)

            # Configura o cliente MercadoPago
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

            # Define os dados dos itens de pagamento
            items = []
            for item in cart:
                try:
                    produto = Produto.objects.get(id=item['id'])
                    items.append({
                        "title": produto.nome,
                        "quantity": item.get('quantity', 1),
                        "currency_id": "BRL",
                        "unit_price": float(produto.valor),
                    })
                except Produto.DoesNotExist:
                    logger.error(f"Produto com ID {item['id']} não encontrado.")
                    return JsonResponse({"error": f"Produto com ID {item['id']} não encontrado."}, status=404)

            # Log dos itens que serão enviados para o MercadoPago
            logger.info(f"Itens para pagamento: {items}")

            # Define os dados do pagamento
            preference_data = {
                "items": items,
                "back_urls": {
                    "success": "https://choppitinerante.cloudboosterlab.org/",
                },
                "auto_return": "approved",
                "notification_url": "https://choppitinerante.cloudboosterlab.org/pag/"  # URL do webhook para notificações
            }

            # Cria a preferência de pagamento
            preference_response = sdk.preference().create(preference_data)
            logger.info(f"Resposta da criação da preferência: {preference_response}")

            # Verifica se a resposta contém o ponto de inicialização do pagamento
            if "init_point" not in preference_response["response"]:
                logger.error(f"Erro na resposta do MercadoPago: {preference_response}")
                return JsonResponse({"error": "Erro ao gerar link de pagamento. Verifique as credenciais e os dados enviados."}, status=500)

            preference = preference_response["response"]

            # Cria uma transação e associa ao cliente
            cliente = Cliente(nome='Cliente Anônimo')  # Cliente anônimo ou crie o cliente de acordo com os dados do pedido
            cliente.save()
            transacao = Transacao(
                transacao_id=preference['id'],
                collector_id=preference.get('collector_id', ''),
                cliente=cliente
            )
            transacao.save()

            # Retorna o link de checkout do MercadoPago
            return JsonResponse({"init_point": preference['init_point']})

        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return JsonResponse({"error": "Dados de entrada inválidos."}, status=400)
        except Exception as e:
            logger.exception("Erro inesperado ao criar link de pagamento.")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({'status': 'method_not_allowed'}, status=405)

@csrf_exempt
def simple_test(request):
    """
    View para receber notificações de webhook.
    """
    if request.method == "POST":
        # Recebe e processa o webhook do MercadoPago
        webhook_data = json.loads(request.body.decode('utf-8'))
        print("Webhook Recebido:", webhook_data)

        # Extrair informações do webhook
        pagamento_id = webhook_data.get('data', {}).get('id', '')
        status = webhook_data.get('action', '')

        # Se desejar, armazene ou atualize a transação no banco de dados
        transacao = Transacao.objects.filter(transacao_id=pagamento_id).first()
        if transacao:
            transacao.status = status
            transacao.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'method_not_allowed'})


def listar_transacoes(request):
    """
    View para listar todas as transações.
    """
    transacoes = Transacao.objects.all()
    return render(request, 'transacoes.html', {'transacoes': transacoes})
