# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-21 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chopchop_app', '0004_auto_20190120_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chair',
            name='current_session',
            field=models.DateTimeField(),
        ),
    ]
