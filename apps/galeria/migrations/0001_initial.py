# Generated by Django 5.0.2 on 2024-03-22 12:00

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fotografia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('legenda', models.CharField(max_length=150)),
                ('descricao', models.TextField()),
                ('foto', models.ImageField(blank=True, upload_to='fotos')),
                ('data_fotografia', models.DateTimeField(default=datetime.datetime.now)),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fotografias', to='produto.produto')),
            ],
        ),
    ]
