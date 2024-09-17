from django.db import models

# Create your models here.
class Contato(models.Model):
    nome = models.CharField(max_length=50)
    celular = models.CharField(max_length=11)
    mensagem = models.TextField()


    def __str__(self) -> str:
        return f"Cliente {self.nome} - {self.celular} "