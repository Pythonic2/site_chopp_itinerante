# Generated by Django 5.1.1 on 2024-09-14 16:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produto', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transacao_id', models.CharField(max_length=100)),
                ('collector_id', models.CharField(max_length=20)),
                ('data_transacao', models.DateTimeField(auto_now_add=True)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produto', models.ManyToManyField(related_name='transacoes', to='produto.produto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacoes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]