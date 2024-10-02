from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Produto

# Create your views here.
class CardapioView(TemplateView):
    """Renderiza o template do cardápio e retorna a quantidade de itens no carrinho"""

    template_name = 'produtos.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['produtos'] = Produto.objects.all().order_by('-servico', '-id')
        context['title'] = 'Produtos'


        return render(request, self.template_name, context)