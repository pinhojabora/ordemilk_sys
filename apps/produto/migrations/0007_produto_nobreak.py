# Generated by Django 5.0.2 on 2024-03-25 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_produto_conj_ordenha'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='nobreak',
            field=models.BooleanField(default=False),
        ),
    ]
