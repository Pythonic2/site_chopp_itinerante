from django.db import models
import boto3
from django.conf import settings
from io import BytesIO
from botocore.exceptions import NoCredentialsError
import os
import shutil
from django.db.models.signals import pre_save
from django.dispatch import receiver


class CategoriaEvento(models.Model):
    nome = models.CharField(max_length=40)
    
    def __str__(self):
        return self.nome


class EventoRealizado(models.Model):
    categoria = models.ForeignKey(CategoriaEvento, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='esse texto aparecerá abaixo da imagem', blank=True)
    
    def __str__(self):
        return self.nome


class ImagemEvento(models.Model):
    evento = models.ForeignKey(EventoRealizado, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='eventos/')
    
    def __str__(self):
        return f"Imagem de {self.evento.nome}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.upload_to_r2()

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
                
                # Definir o caminho correto da imagem no bucket S3, incluindo a pasta 'eventos/'
                s3_file_name = f'{self.imagem.name}'
                
                # Upload direto da memória
                s3.upload_fileobj(
                    BytesIO(imagem_conteudo),
                    settings.AWS_STORAGE_BUCKET_NAME,
                    s3_file_name
                )
                print("Upload Successful")

                # Caminhos das pastas que você deseja excluir localmente
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

                excluir_pasta(pasta_eventos)
            else:
                print("Nenhuma imagem foi fornecida.")
        except NoCredentialsError:
            print("Credentials not available")


@receiver(pre_save, sender=ImagemEvento)
def verificar_alteracao_imagem(sender, instance, **kwargs):
    # Verifica se a imagem já existe no banco de dados
    if instance.pk:
        try:
            imagem_antiga = ImagemEvento.objects.get(pk=instance.pk)
            # Verifica se a imagem foi alterada
            if imagem_antiga.imagem != instance.imagem:
                instance.upload_to_r2()
        except ImagemEvento.DoesNotExist:
            pass  # Se a imagem não existir, não faz nada
    else:
        # Se for uma nova imagem, faz o upload
        instance.upload_to_r2()


class Contato(models.Model):
    nome = models.CharField(max_length=50)
    celular = models.CharField(max_length=11)
    mensagem = models.TextField()
    
    def __str__(self) -> str:
        return f"Cliente {self.nome} - {self.celular}"


class Testemunho(models.Model):
    cliente = models.CharField(max_length=100, blank=True, null=True)
    tipo_evento = models.CharField(max_length=50)
    data_evento = models.DateField(auto_now_add=True)
    feedback = models.TextField()
    
    def __str__(self) -> str:
        return f"Feedback de {self.cliente} - {self.data_evento}"
