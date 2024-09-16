from django.db import models
from django.contrib.auth.models import User,AbstractUser, Permission

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
   

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username


class Evento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    celular = models.CharField(max_length=11, blank=True, null=True)
    bairro = models.CharField(max_length=100, default='None')
    endereco = models.CharField(max_length=100)
    data_evento = models.DateField(null=True)
    tipo_evento = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.tipo_evento} - {self.data_evento}"