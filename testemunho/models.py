from django.db import models

# Create your models here.

class Testemunho(models.Model):
    cliente = models.CharField(max_length=100, blank=True, null=True)
    tipo_evento = models.CharField(max_length=50)
    data_evento = models.DateField(auto_now_add=True)
    feedback = models.TextField()

    def __str__(self) -> str:
        return f"Feedback de {self.cliente} - {self.data_evento}"