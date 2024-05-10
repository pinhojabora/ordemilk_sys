# Generated by Django 5.0.2 on 2024-05-08 18:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='fase',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='pipeline', to='pipeline.fase_pipeline'),
        ),
    ]