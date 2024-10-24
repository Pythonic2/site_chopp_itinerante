import boto3
from botocore.exceptions import NoCredentialsError
import os
import django
from django.conf import settings

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Configurações R2
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME = settings.AWS_S3_REGION_NAME

# Caminho do arquivo local e nome do arquivo no R2
local_file_path = 'chopps/testefig3.png'  # Substitua pelo caminho do seu arquivo
s3_file_name = 'media/chopps/testefig3.png'  # Nome com o qual o arquivo será salvo no R2

# Função para upload
def upload_to_r2(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_S3_REGION_NAME)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

# Executar upload
upload_to_r2(local_file_path, AWS_STORAGE_BUCKET_NAME, s3_file_name)
