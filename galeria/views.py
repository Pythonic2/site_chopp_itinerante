from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import CategoriaEvento, EventoRealizado, ImagemEvento
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class GaleriaView(TemplateView):
    template_name = 'galeria.html'

    def get(self, request):
        eventos = EventoRealizado.objects.all().order_by('-id')
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