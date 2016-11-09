# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 14:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20161107_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='finish_backup_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start backup datetime'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='start_backup_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 7, 14, 28, 0, 176184, tzinfo=utc), verbose_name='Finish backup datetime'),
        ),
    ]