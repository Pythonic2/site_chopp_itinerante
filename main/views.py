from django.shortcuts import render, redirect
import mercadopago
from django.conf import settings
import logging
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

logger = logging.getLogger(__name__)
@cache_page(60 * 60 * 24)
def home(request):
    return render(request, 'index.html',{'title':'Chopp Itinerante'})
