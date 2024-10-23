from django.db import models
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

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
