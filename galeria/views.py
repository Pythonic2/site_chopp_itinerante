from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class GaleriaView(TemplateView):
    template_name = 'galeria.html'
    

    def get(self, request):
        
        return render(request, self.template_name)