# Generated by Django 5.0.2 on 2024-04-15 20:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0004_alter_pedido_valor_total'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedido', to=settings.AUTH_USER_MODEL),
        ),
    ]
