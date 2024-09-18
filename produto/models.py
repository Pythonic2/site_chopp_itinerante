from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, default='descreva o produto/serviço')
    disponivel = models.BooleanField(default=True)  # Use um valor padrão
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Usar DecimalField é melhor para preços
    litros = models.PositiveIntegerField(blank=True, null=True)  # Litros devem ser um valor positivo
    imagem = models.ImageField(upload_to='chopps', blank=True, null=True, default=None)
    servico = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
