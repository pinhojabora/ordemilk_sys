# Generated by Django 5.0.2 on 2024-03-25 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurador', '0004_configurador_gerenciamento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurador',
            name='quant_gerenciamento',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]