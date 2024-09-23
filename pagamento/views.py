from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from .models import Transacao, Usuario, Produto
from carrinho.models import Carrinho
from authentication.models import Evento
import mercadopago
import pandas as pd
from .busca_pagameto import buscar_pagamento_mercado_pago
from notifications import send_email
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


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
            tipo = webhook_data.get('type', {})
            print(tipo)
            # Criar um DataFrame do webhook_data e salvar em CSV
            df = pd.DataFrame([webhook_data])  # Convertendo o dict para DataFrame
            df.to_csv('recibo.csv')

            # Buscar pagamento usando a função definida anteriormente
            pag = buscar_pagamento_mercado_pago(pagamento_id)
            try:
                pag['id'] 
                if pag['id'] and tipo == 'payment':
                    user = Usuario.objects.get(username=pag['usuario'])

                    
                    # Criar a instância da transação
                    transacao = Transacao(
                        transacao_id=pag['id'],
                        usuario=user,
                        data_transacao=pag['data'],
                        valor_total=pag['valor'],
                        status=pag['status']
                    )
                    transacao.save()  # Salvar a transação primeiro

                    # Associar produtos à transação
                    produtos = pag['items']
                    for produto_data in produtos:
                        produto = Produto.objects.get(nome=produto_data)
                        transacao.produtos.add(produto.id) 

                    evento = Evento.objects.get(usuario=user, carrinho=pag['carrinho'])
                    carrinho = Carrinho.objects.get(usuario=user,id=f'{int(evento.carrinho)}')
                    carrinho.status = 'Pago'
                    evento.status = 'Pago'
                    
                    evento.save()
                    carrinho.save()
                    # carrinho.delete()
                    send_email(
                        subject=f"Nova Compra Realizada",
                        body=f"Evento: {evento.tipo_evento}\nData: {evento.data_evento}\nBairro: {evento.bairro}\nRua: {evento.endereco}\nValor da Compra: {evento.valor}\nCliente: {user.nome}\nContato: {evento.celular}\nProdutos: {produtos}",
                        sender_email="noticacoes@gmail.com",
                        sender_password=os.getenv('SENHA'),
                        recipient_emails=["choppitinerante@gmail.com","igormarinhosilva@gmail.com"]
                    )
                    print(evento)
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'Order Generate'})
            except Exception as e :
                print(e)
               
                return JsonResponse({'status': 'Order Generate'})
            
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Falha ao decodificar JSON'}, status=400)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        except Produto.DoesNotExist:
            return JsonResponse({'error': 'Produto não encontrado'}, status=404)
    
    return JsonResponse({'status': 'method_not_allowed'}, status=405)

def gerar_pagamento(cliente_id, produtos, carrinho):
    # Inicializar o SDK do Mercado Pago
    sdk = mercadopago.SDK('TEST-3488797328851277-091614-dbbff0af2658e101ee7f9413497c16fd-162016798')

    # Construir a lista de itens dinamicamente
    items = []
    for produto, quantidade in produtos:
        # Supondo que 'produto' seja um objeto ou dicionário com os atributos 'id', 'nome', 'valor' e 'quantidade'
        item = {
            "id": produto.id,
            "title": produto.nome,
            "quantity": quantidade,
            "currency_id": "BRL",
            "unit_price": float(produto.valor)
        }
        items.append(item)

    # Configurar os dados da preferência
    preference_data = {
        "items": items,
        "back_urls": {
            "success": "https://choppitinerante.cloudboosterlab.org/minhas-compras/",
            "failure": "https://choppitinerante.cloudboosterlab.org/minhas-compras/",
            "pending": "https://choppitinerante.cloudboosterlab.org/minhas-compras/",
        },
        "external_reference": f'{cliente_id}',  # Enviando o ID do usuário aqui
        "auto_return": "approved",
        "notification_url": "https://choppitinerante.cloudboosterlab.org/pag/",
        "metadata": {
            "other_info": carrinho
        }
    }


    result = sdk.preference().create(preference_data)
    preference = result['response']

    return preference['init_point']

