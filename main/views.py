from django.shortcuts import render, redirect
import mercadopago
from django.conf import settings
import logging
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'index.html')
