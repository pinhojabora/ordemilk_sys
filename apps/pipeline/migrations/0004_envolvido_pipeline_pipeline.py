# Generated by Django 5.0.2 on 2024-05-13 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0003_alter_pipeline_validade_proposta'),
    ]

    operations = [
        migrations.AddField(
            model_name='envolvido_pipeline',
            name='pipeline',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='envolvido_pipeline', to='pipeline.pipeline'),
            preserve_default=False,
        ),
    ]
