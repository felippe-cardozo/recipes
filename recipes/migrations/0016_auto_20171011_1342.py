# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20171011_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]