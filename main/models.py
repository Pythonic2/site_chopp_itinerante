from django.db import models

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
    

class Contato(models.Model):
    nome = models.CharField(max_length=50)
    celular = models.CharField(max_length=11)
    mensagem = models.TextField()


    def __str__(self) -> str:
        return f"Cliente {self.nome} - {self.celular} "

class Testemunho(models.Model):
    cliente = models.CharField(max_length=100, blank=True, null=True)
    tipo_evento = models.CharField(max_length=50)
    data_evento = models.DateField(auto_now_add=True)
    feedback = models.TextField()

    def __str__(self) -> str:
        return f"Feedback de {self.cliente} - {self.data_evento}"