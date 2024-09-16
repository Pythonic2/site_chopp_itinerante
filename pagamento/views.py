from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from .models import Transacao
import mercadopago
import pandas as pd

@csrf_exempt
def simple_test(request):
    if request.method == "POST":
        if not request.body:
            return JsonResponse({'error': 'Corpo da requisição vazio'}, status=400)

        try:
            # Decodificar o corpo da requisição em JSON
            webhook_data = json.loads(request.body.decode('utf-8'))

            # Capturar o pagamento_id e outras informações do webhook
            pagamento_id = webhook_data.get('data', {}).get('id', '')
            status = webhook_data.get('action', '')
            external_reference = webhook_data.get('external_reference', '')

            # Criar um DataFrame do webhook_data e salvar em CSV
            df = pd.DataFrame([webhook_data])  # Convertendo o dict para DataFrame
            df.to_csv('recibo.csv')

            # Seu código para lidar com a transação
            transacao = Transacao.objects.filter(transacao_id=pagamento_id).last()
            if transacao:
                transacao.status = status
                transacao.cliente_id = external_reference  # Atualize o cliente_id
                transacao.save()

            return JsonResponse({'status': 'success'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Falha ao decodificar JSON'}, status=400)
    
    return JsonResponse({'status': 'method_not_allowed'}, status=405)5)

def gerar_pagamento(cliente_id, valor):
    sdk = mercadopago.SDK('TEST-3488797328851277-091614-dbbff0af2658e101ee7f9413497c16fd-162016798')
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
    "payer": {
        "name": "Test",
        "surname": "User",
        "email": "your_test_email@example.com",
        "phone": {
            "area_code": "11",
            "number": "4444-4444",
        },
        "identification": {
            "type": "CPF",
            "number": "19119119100",
        }
    },
    "back_urls": {
        "success": "http://test.com/success",
        "failure": "http://test.com/failure",
        "pending": "http://test.com/pending",
    },
    "external_reference": f'{cliente_id}',  # Enviando o ID do usuário aqui
    "auto_return": "approved",
    "notification_url": "https://choppitinerante.cloudboosterlab.org/pag/",
     # Aqui você pode adicionar qualquer dado extra
    "metadata": {
        "custom_user_id": f"xpto",
        "other_info": "alguma informação personalizada"
    }
}


    result = sdk.preference().create(preference_data)
    preference = result['response']

    return preference

def listar_transacoes(request):
    transacoes = Transacao.objects.all()
    return render(request, 'transacoes.html', {'transacoes': transacoes})
