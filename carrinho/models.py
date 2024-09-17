from django.db import models
from authentication.models import Usuario
from produto.models import Produto
from authentication.models import Evento


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