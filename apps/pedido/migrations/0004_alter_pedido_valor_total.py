# Generated by Django 5.0.2 on 2024-04-15 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_alter_pedido_parcelas_alter_pedido_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]