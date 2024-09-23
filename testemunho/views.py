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
