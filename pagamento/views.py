from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from .models import Transacao
import mercadopago


@csrf_exempt
def simple_test(request):
    if request.method == "POST":
        if not request.body:
            return JsonResponse({'error': 'Corpo da requisição vazio'}, status=400)

        try:
            webhook_data = json.loads(request.body.decode('utf-8'))
            print("Webhook Recebido:", webhook_data)

            pagamento_id = webhook_data.get('data', {}).get('id', '')
            status = webhook_data.get('action', '')
            external_reference = webhook_data.get('data', {}).get('external_reference', '')

            # Seu código para lidar com a transação
            transacao = Transacao.objects.filter(transacao_id=pagamento_id).first()
            if transacao:
                transacao.status = status
                transacao.cliente_id = external_reference  # Atualize o cliente_id
                transacao.save()

            return JsonResponse({'status': 'success'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Falha ao decodificar JSON'}, status=400)
    
    return JsonResponse({'status': 'method_not_allowed'}, status=405)


def gerar_pagamento(cliente_id, valor):
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
        "external_reference": f'{cliente_id}',
        
        "auto_return": "approved",
        "notification_url": "https:///webhook.site/51705b86-2cad-48f3-9228-04ed1b6c9a72"
    }

    result = sdk.preference().create(preference_data)
    preference = result['response']

    return preference

def listar_transacoes(request):
    transacoes = Transacao.objects.all()
    return render(request, 'transacoes.html', {'transacoes': transacoes})
