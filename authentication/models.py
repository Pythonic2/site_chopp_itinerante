# authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Evento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    celular = models.CharField(max_length=11)
    bairro = models.CharField(max_length=100, default='None')
    endereco = models.CharField(max_length=100)
    data_evento = models.DateField(null=True)
    tipo_evento = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True, blank=True, default=' ')
    #carrinho = models.CharField(max_length=50, default=0, unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.tipo_evento} - {self.data_evento}"
