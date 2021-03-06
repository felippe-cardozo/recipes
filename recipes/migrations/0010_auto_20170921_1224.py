# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 12:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0009_recipe_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cookbook',
            field=models.ManyToManyField(related_name='user_cookbook', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='likes',
            field=models.ManyToManyField(related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
