# Generated by Django 5.0.2 on 2024-03-22 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferramentas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_contencao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_contencao_nome', models.CharField(max_length=100)),
            ],
        ),
    ]
