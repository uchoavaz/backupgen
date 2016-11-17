# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-17 19:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20161117_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='start_backup_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 17, 19, 44, 25, 435151, tzinfo=utc), verbose_name='Start backup datetime'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='storage_destiny_path',
            field=models.TextField(blank=True, default='', null=True, verbose_name='storage_destiny_path'),
        ),
        migrations.AlterField(
            model_name='backuplog',
            name='log_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 17, 19, 44, 25, 435882, tzinfo=utc), verbose_name='Finish backup datetime'),
        ),
        migrations.AlterField(
            model_name='systeminfo',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 11, 17, 19, 44, 25, 434356, tzinfo=utc), verbose_name='Date'),
        ),
    ]
