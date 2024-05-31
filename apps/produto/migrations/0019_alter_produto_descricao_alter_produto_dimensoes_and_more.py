# Generated by Django 5.0.2 on 2024-05-28 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0018_produto_numero_conjuntos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='dimensoes',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='peso',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]