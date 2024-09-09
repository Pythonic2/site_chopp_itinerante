from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Para desabilitar a verificação de CSRF para esta view (necessário para webhooks)
def pag(request):
    """
    Esta view de teste recebe notificações de um webhook.
    Ela processa as informações enviadas pelo serviço do webhook e retorna uma resposta.
    """
    if request.method == "POST":
        # Processa os dados do webhook recebidos em request.body ou request.POST
        data = request.body  # Ou request.POST, dependendo do formato do webhook

        # Aqui você pode adicionar lógica para processar os dados recebidos

        return JsonResponse({'status': 'success', 'message': 'Webhook recebido com sucesso!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)
