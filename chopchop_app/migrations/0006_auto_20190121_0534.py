# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-21 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chopchop_app', '0005_auto_20190121_0241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chair',
            old_name='current_session',
            new_name='current_session_time',
        ),
        migrations.AddField(
            model_name='chair',
            name='current_session_id',
            field=models.IntegerField(default=0),
        ),
    ]
