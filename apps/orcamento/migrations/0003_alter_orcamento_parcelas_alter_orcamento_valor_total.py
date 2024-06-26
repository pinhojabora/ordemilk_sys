# Generated by Django 5.0.2 on 2024-04-15 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0002_orcamento_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='parcelas',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='orcamento',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
