# Generated by Django 5.0.2 on 2024-05-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurador', '0012_configurador_numero_conjuntos'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurador',
            name='fator_calculo_modelo',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
