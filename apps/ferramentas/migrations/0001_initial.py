# Generated by Django 5.0.2 on 2024-03-22 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Modelo_equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo_equipamento_nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Modelo_sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo_sala_nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tensao_energia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tensao_energia_nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_linha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_linha_nome', models.CharField(max_length=100)),
            ],
        ),
    ]