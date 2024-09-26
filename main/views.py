from django.shortcuts import render, redirect
from django.conf import settings
import logging
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from testemunho.models import Testemunho
from pagamento.models import Transacao
from contato.forms import ContatoForm
from django.utils.decorators import method_decorator
from notifications import send_email
import os
from dotenv import load_dotenv
load_dotenv() 
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self,request):
        testemunhos = Testemunho.objects.all().order_by('-id')
        eventos_realizados = Transacao.objects.all().count()
        eventos_base = 50 + eventos_realizados
        context = {'testemunhos':testemunhos,'title':'Chopp Itinerante','testemunhos':testemunhos, 'form':ContatoForm, 'conta_eventos':eventos_base}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            nome = form.cleaned_data['nome']
            celular = form.cleaned_data['celular']
            mensagem = form.cleaned_data['mensagem']

         
            send_email(
                subject=f"Novo Contato de {nome}",
                body=f"{mensagem}\nContato: {celular}",
                sender_email="noticacoes@gmail.com",
                sender_password=os.getenv('SENHA'),
                recipient_emails=["choppitinerante@gmail.com","igormarinhosilva@gmail.com"]
            )

            return redirect('home')
    
