# Generated by Django 2.2.16 on 2022-03-20 22:20

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20220317_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFFFF', max_length=18, unique=True, verbose_name='Цвет'),
        ),
    ]
