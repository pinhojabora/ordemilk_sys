# Generated by Django 5.0.2 on 2024-05-03 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0013_producao1_codigo_producao1_nome_delete_producao2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producao1',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producao1s', to='produto.produto'),
        ),
        migrations.CreateModel(
            name='Producao2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('nome', models.TextField(blank=True, max_length=100, null=True)),
                ('quantidade', models.DecimalField(blank=True, decimal_places=5, default=0, max_digits=30, null=True)),
                ('producao1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producao2s', to='produto.producao1')),
            ],
        ),
    ]
