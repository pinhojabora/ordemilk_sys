# Generated by Django 5.0.2 on 2024-04-26 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0008_alter_categoria_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategoria',
            options={'ordering': ['nome']},
        ),
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.TextField(max_length=100),
        ),
    ]