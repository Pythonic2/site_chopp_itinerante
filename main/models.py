from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=11, blank=True, null=True)
    endereco = models.CharField(max_length=100)
    data_evento = models.DateField()  # Use um nome mais descritivo
    tipo_evento = models.CharField(max_length=50)  # Também use um nome descritivo

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

class Transacao(models.Model):
    transacao_id = models.CharField(max_length=100)  # Ajustado para permitir transações maiores
    collector_id = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='transacoes')  # Adicionado on_delete e related_name
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='transacoes')  # Relacionamento entre transação e produto
    data_transacao = models.DateTimeField(auto_now_add=True)  # Adicionando a data da transação
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  # Salvar o valor da transação

    def __str__(self):
        return f'Transação {self.transacao_id} - Cliente: {self.cliente.nome}'
