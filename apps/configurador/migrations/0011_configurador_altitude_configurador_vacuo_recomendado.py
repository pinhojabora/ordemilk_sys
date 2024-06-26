# Generated by Django 5.0.2 on 2024-05-21 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurador', '0010_remove_configurador_cep_remove_configurador_cnpj_cpf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurador',
            name='altitude',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='configurador',
            name='vacuo_recomendado',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
