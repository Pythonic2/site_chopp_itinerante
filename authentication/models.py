# authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from pagamento.models import Produto

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Carrinho(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrinhos')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='Progress')
    def __str__(self):
        return f'Carrinho de {self.usuario} em {self.data}'
    

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    class Meta:
        unique_together = ('carrinho', 'produto')

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} no carrinho de {self.carrinho.usuario}'
    

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
