# Generated by Django 5.0.2 on 2024-03-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferramentas', '0002_tipo_contencao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_gerenciamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_gerenciamento_nome', models.CharField(max_length=100)),
            ],
        ),
    ]
