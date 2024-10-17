from django.contrib import admin
from .models import Transacao,Produto

admin.site.register(Produto)

admin.site.register(Transacao)