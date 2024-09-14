from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)  # Use um valor padrão
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Usar DecimalField é melhor para preços
    litros = models.PositiveIntegerField()  # Litros devem ser um valor positivo
    imagem = models.ImageField(upload_to='chopps', blank=True, null=True, default=None)
    collector_id = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.nome
