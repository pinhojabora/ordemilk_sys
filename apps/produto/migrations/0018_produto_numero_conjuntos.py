# Generated by Django 5.0.2 on 2024-05-21 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0017_alter_producao1_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='numero_conjuntos',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]