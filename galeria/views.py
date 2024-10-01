from django.shortcuts import render
from django.views.generic import TemplateView
from .models import CategoriaEvento, EventoRealizado


class GaleriaView(TemplateView):
    template_name = 'galeria.html'
    

    def get(self, request):
        eventos = EventoRealizado.objects.all().order_by('-id')
        categorias = CategoriaEvento.objects.all()
        context = {'eventos':eventos,'categorias':categorias}
        return render(request, self.template_name, context)