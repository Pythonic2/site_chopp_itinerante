from django.db import models

# Create your models here.


class CategoriaEvento(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self):
        return self.nome


class EventoRealizado(models.Model):
    categoria = models.ForeignKey(CategoriaEvento, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='esse texto aparecerá abaixo da imagem', blank=True)

    def __str__(self):
        return self.nome
    

class ImagemEvento(models.Model):
    evento = models.ForeignKey(EventoRealizado, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='eventos/')

    def __str__(self):
        return f"Imagem de {self.evento.nome}"

