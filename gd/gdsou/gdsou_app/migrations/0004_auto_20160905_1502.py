# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdsou_app', '0003_race'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='release_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='race',
            name='return_date',
            field=models.DateTimeField(),
        ),
    ]
