# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20170816_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]