# Generated by Django 5.1.1 on 2024-09-21 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.CharField(default='descreva o produto/serviço', max_length=255)),
                ('disponivel', models.BooleanField(default=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('litros', models.PositiveIntegerField(blank=True, null=True)),
                ('imagem', models.ImageField(blank=True, default=None, null=True, upload_to='chopps')),
                ('servico', models.BooleanField(default=False)),
            ],
        ),
    ]
