# Generated by Django 5.0.2 on 2024-03-25 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferramentas', '0003_tipo_gerenciamento'),
        ('produto', '0003_produto_sistema_limpeza'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='tipo_gerenciamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferramentas.tipo_gerenciamento'),
        ),
    ]
