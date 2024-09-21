from django.contrib import admin
from .models import CategoriaEvento, EventoRealizado, ImagemEvento

class ImagemEventoInline(admin.TabularInline):
    model = ImagemEvento
    extra = 1  # Número de campos extras para upload de imagens

class EventoRealizadoAdmin(admin.ModelAdmin):
    inlines = [ImagemEventoInline]

admin.site.register(CategoriaEvento)
admin.site.register(EventoRealizado, EventoRealizadoAdmin)
