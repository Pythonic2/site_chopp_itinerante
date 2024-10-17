from django.shortcuts import render, redirect
from django.conf import settings
import logging
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .models import Testemunho
from pagamento.models import Transacao
from .forms import ContatoForm
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
    
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import CategoriaEvento, EventoRealizado, ImagemEvento
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required




@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GaleriaView(TemplateView):
    template_name = 'galeria.html'

    def get(self, request):
        eventos = EventoRealizado.objects.all().order_by('-id')
        print(f'-------count {eventos.count()}')
        categorias = CategoriaEvento.objects.all()
        context = {'eventos': eventos, 'categorias': categorias}
        return render(request, self.template_name, context)

def is_admin_or_in_group(user):
    """Verifica se o usuário é um superusuário ou pertence a um grupo específico."""
    return user.is_superuser or user.groups.filter(name='nome_do_grupo').exists()

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin_or_in_group), name='dispatch')
class GaleriaCreateView(TemplateView):
    template_name = 'cadastra_imagens_evento.html'
    
    def get(self, request):
        categorias = CategoriaEvento.objects.all()
        context = {'categorias': categorias}
        return render(request, self.template_name, context)
     
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Obtém o ID da categoria e o nome do evento do request
            categoria_id = request.POST.get('categoria')
            nome_evento = request.POST.get('nome')

            # Cria e salva a instância do EventoRealizado
            evento = EventoRealizado.objects.create(categoria_id=categoria_id, nome=nome_evento)

            # Obtém a lista de imagens do request
            images = request.FILES.getlist('images')
            images.reverse()
            # Cria objetos ImagemEvento para cada imagem enviada
            try:
                for image in images:
                    img = ImagemEvento(evento=evento, imagem=image)
                    img.save()
                # Redireciona para a galeria após o upload
                return redirect('cad_fotos')
            except Exception as e:
                print(e)

        # Caso não seja um POST, renderiza a página com um erro ou a página de galeria
        return render(request, self.template_name, {'error': 'Método não suportado'})
    

from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse
from .forms import FeedBackForms
from .models import Testemunho

class FeedbackView(CreateView):
    form_class = FeedBackForms
    model = Testemunho
    template_name = 'feedback.html'  # Substitua pelo caminho do seu template

    def get_success_url(self):
        return reverse('home') + '#feedbacks'  # Substitua 'home' pelo nome correto da sua URL para a home

    def form_valid(self, form):
        # Você pode adicionar lógica aqui, se necessário
        return super().form_valid(form)
