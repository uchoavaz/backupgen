# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-08 13:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20161107_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='backuplog',
            name='log_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 13, 42, 11, 82392, tzinfo=utc), verbose_name='Finish backup datetime'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='start_backup_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 13, 42, 11, 81725, tzinfo=utc), verbose_name='Start backup datetime'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='status',
            field=models.IntegerField(choices=[(1, 'Rodando'), (2, 'Terminado'), (3, 'Terminado com erro')], default=1, verbose_name='Status'),
        ),
    ]
