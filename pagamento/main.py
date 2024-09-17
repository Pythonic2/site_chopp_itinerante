import mercadopago

# Substitua pelo seu token de acesso do Mercado Pago
ACCESS_TOKEN = 'TEST-3488797328851277-091614-dbbff0af2658e101ee7f9413497c16fd-162016798'

# Inicializar o SDK do Mercado Pago
sdk = mercadopago.SDK(ACCESS_TOKEN)

# Função para buscar o pagamento no Mercado Pago usando o SDK
def buscar_pagamento_mercado_pago(pagamento_id):
    try:
        # Usando o SDK para buscar o pagamento
        pagamento = sdk.payment().get(pagamento_id)

        # Verificar se a resposta foi bem-sucedida
        if pagamento["status"] == 200:
            dados_pagamento = pagamento["response"]
                        
            itens = dados_pagamento.get('additional_info', {}).get('items', [])
            inf = dados_pagamento.get('metadata', {}).get('other_info', [])
            print(inf)
            x = []
            if itens:
                for item in itens:
                    item_title = item.get('title', 'Sem título')
                    x.append(item_title)
            else:
                print("Nenhum item encontrado na resposta.")
            return {
                "id":dados_pagamento.get('id'),
                "status":dados_pagamento.get('status'),
                "valor":dados_pagamento.get('transaction_amount'),
                "usuario":dados_pagamento.get('external_reference'),
                "data":dados_pagamento.get('date_approved'),
                "items":x,
                "carrinho": dados_pagamento.get('metadata', {}).get('other_info', [])
                
            }
        else:
            print(f"Erro ao buscar o pagamento: {pagamento['status']}, {pagamento['response']}")
    
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

