# Generated by Django 5.0.2 on 2024-03-25 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurador', '0005_configurador_quant_gerenciamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_configurador',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='item_configurador',
            name='valor_unitario',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
