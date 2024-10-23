from django.db import models
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

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
    imagem = models.ImageField(upload_to='chopps/', blank=True, null=True, default=None)
    servico = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    def upload_to_r2(self):
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_S3_REGION_NAME)
        local_file_path = self.imagem.path
        s3_file_name = f'{self.imagem.name}'

        try:
            s3.upload_file(local_file_path, settings.AWS_STORAGE_BUCKET_NAME, s3_file_name)
            print("Upload Successful")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")
