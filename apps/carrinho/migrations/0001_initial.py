# Generated by Django 5.0.2 on 2024-03-26 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produto', '0007_produto_nobreak'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('valor_unitario', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='produto.produto')),
            ],
        ),
    ]