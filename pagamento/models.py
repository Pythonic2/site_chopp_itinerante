from django.db import models
from authentication.models import Usuario
from produto.models import Produto



class Transacao(models.Model):
    transacao_id = models.CharField(max_length=100)  # Ajustado para permitir transações maiores
    collector_id = models.CharField(max_length=20)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacoes')  # Adicionado on_delete e related_name
    produto = models.ManyToManyField(Produto, related_name='transacoes')  # Relacionamento entre transação e produto
    data_transacao = models.DateTimeField(auto_now_add=True)  # Adicionando a data da transação
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  # Salvar o valor da transação

    def __str__(self):
        return f'Transação {self.transacao_id} - Usuario: {self.usuario.nome}'
