from django.db import models

class Transacao(models.Model):
    transacao_id = models.CharField(max_length=100, unique=True)  # Ajustado para permitir transações maiores
    usuario = models.ForeignKey('authentication.Usuario', on_delete=models.CASCADE, related_name='transacoes')  # Adicionado on_delete e related_name
    produtos = models.ManyToManyField('Produto', related_name='transacoes')  # Relacionamento entre transação e produto
    data_transacao = models.DateTimeField(auto_now_add=True)  # Adicionando a data da transação
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  # Salvar o valor da transação
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'Transação {self.transacao_id} - Usuario: {self.usuario}'

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
