# Generated by Django 5.0.2 on 2024-05-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0002_alter_pipeline_fase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='validade_proposta',
            field=models.DateField(blank=True, null=True),
        ),
    ]
