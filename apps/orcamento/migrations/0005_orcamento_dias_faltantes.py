# Generated by Django 5.0.2 on 2024-04-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0004_orcamento_vencimento_orcamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='dias_faltantes',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
