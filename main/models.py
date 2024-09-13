from django.db import models
from django.contrib.auth.models import User,AbstractUser, Permission

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=11, blank=True, null=True)
    bairro = models.CharField(max_length=100, default='None')
    endereco = models.CharField(max_length=100)
    data_evento = models.DateField(null=True)  # Use um nome mais descritivo
    tipo_evento = models.CharField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)  # Use um valor padrão
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Usar DecimalField é melhor para preços
    litros = models.PositiveIntegerField()  # Litros devem ser um valor positivo
    imagem = models.ImageField(upload_to='media', blank=True, null=True, default=None)

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrinhos')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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

class Transacao(models.Model):
    transacao_id = models.CharField(max_length=100)  # Ajustado para permitir transações maiores
    collector_id = models.CharField(max_length=20)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacoes')  # Adicionado on_delete e related_name
    produto = models.ManyToManyField(Produto, related_name='transacoes')  # Relacionamento entre transação e produto
    data_transacao = models.DateTimeField(auto_now_add=True)  # Adicionando a data da transação
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  # Salvar o valor da transação

    def __str__(self):
        return f'Transação {self.transacao_id} - Usuario: {self.usuario.nome}'
