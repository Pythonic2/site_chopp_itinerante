# Generated by Django 5.1.1 on 2024-09-17 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrinho', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrinho',
            name='status',
            field=models.CharField(default='Progress', max_length=20),
        ),
    ]
