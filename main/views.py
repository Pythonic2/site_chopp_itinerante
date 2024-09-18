from django.shortcuts import render, redirect
import mercadopago
from django.conf import settings
import logging
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from testemunho.models import Testemunho
from contato.forms import ContatoForm
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self,request):
        testemunhos = Testemunho.objects.all().order_by('-id')
        context = {'testemunhos':testemunhos,'title':'Chopp Itinerante','testemunhos':testemunhos, 'form':ContatoForm}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
