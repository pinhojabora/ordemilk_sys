# Generated by Django 5.0.2 on 2024-03-22 12:00

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ferramentas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configurador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_configuracao', models.DateField(default=datetime.datetime.today)),
                ('nome_cliente', models.CharField(max_length=100)),
                ('endereco_cliente', models.CharField(max_length=100)),
                ('cidade', models.CharField(default='', max_length=100)),
                ('estado', models.CharField(default='', max_length=2)),
                ('cep', models.CharField(default='', max_length=9)),
                ('cnpj_cpf', models.CharField(default='', max_length=18)),
                ('insc_estadual', models.CharField(default='', max_length=25)),
                ('fone', models.CharField(default='', max_length=25)),
                ('email', models.CharField(default='', max_length=100)),
                ('observacao', models.TextField()),
                ('modelo_equipamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferramentas.modelo_equipamento')),
                ('modelo_sala', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferramentas.modelo_sala')),
                ('tensao_energia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferramentas.tensao_energia')),
                ('tipo_linha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferramentas.tipo_linha')),
            ],
        ),
    ]
