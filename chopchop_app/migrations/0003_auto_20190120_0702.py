# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-20 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chopchop_app', '0002_auto_20190113_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChairSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chair_code', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set([('table', 'start_time')]),
        ),
    ]
