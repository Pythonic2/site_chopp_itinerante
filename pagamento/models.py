from django.db import models
import boto3
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from io import BytesIO
from botocore.exceptions import NoCredentialsError
import os
import shutil
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Transacao(models.Model):
    transacao_id = models.CharField(max_length=100, unique=True)
    usuario = models.ForeignKey('authentication.Usuario', on_delete=models.CASCADE, related_name='transacoes')
    produtos = models.ManyToManyField('Produto', related_name='transacoes')
    data_transacao = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'Transação {self.transacao_id} - Usuario: {self.usuario}'


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, default='descreva o produto/serviço')
    disponivel = models.BooleanField(default=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    litros = models.PositiveIntegerField(blank=True, null=True)
    imagem = models.ImageField(upload_to='chopps/', blank=True, null=True, default=None)
    servico = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def upload_to_r2(self):
        # Criar cliente S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Fazer upload do arquivo para o S3
        try:
            if self.imagem:
                # Ler o arquivo da memória
                imagem_conteudo = self.imagem.read()
                print(imagem_conteudo)
                
                # Definir o caminho correto da imagem no bucket S3, incluindo a pasta 'chopps/'
                s3_file_name = f'chopps/{self.imagem.name}'
                print(s3_file_name)
                
                # Upload direto da memória
                s3.upload_fileobj(
                    BytesIO(imagem_conteudo),
                    settings.AWS_STORAGE_BUCKET_NAME,
                    s3_file_name
                )
                print("Upload Successful")

                # Caminhos das pastas que você deseja excluir localmente
                pasta_chopps = os.path.join(os.getcwd(), 'chopps')
                pasta_eventos = os.path.join(os.getcwd(), 'eventos')

                # Função para excluir a pasta
                def excluir_pasta(pasta):
                    if os.path.exists(pasta):
                        try:
                            shutil.rmtree(pasta)
                            print(f'A pasta {pasta} foi excluída com sucesso.')
                        except Exception as e:
                            print(f'Erro ao tentar excluir a pasta {pasta}: {e}')
                    else:
                        print(f'A pasta {pasta} não existe.')

                # Excluir as pastas 'chopps' e 'eventos'
                excluir_pasta(pasta_chopps)
                excluir_pasta(pasta_eventos)
            else:
                print("Nenhuma imagem foi fornecida.")
        except NoCredentialsError:
            print("Credentials not available")

# Sinal para verificar alteração de imagem


@receiver(pre_save, sender=Produto)
def verificar_alteracao_imagem(sender, instance, **kwargs):
    # Verifica se o produto já existe no banco de dados
    if instance.pk:
        try:
            produto_antigo = Produto.objects.get(pk=instance.pk)  # Corrigido aqui
            # Verifica se a imagem foi alterada
            if produto_antigo.imagem != instance.imagem:
                instance.upload_to_r2()
        except Produto.DoesNotExist:
            pass  # Caso o produto não exista, não faz nada
    else:
        # Se o produto for novo, faz o upload da imagem
        instance.upload_to_r2()