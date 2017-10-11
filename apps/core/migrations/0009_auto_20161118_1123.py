# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-18 14:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20161117_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='database_ip',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Ip do banco'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='databases_passed',
            field=models.TextField(blank=True, null=True, verbose_name='Bancos passados'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='finish_backup_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Hora de fim do backuo'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nome do backup'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='path_folders_pass',
            field=models.TextField(blank=True, null=True, verbose_name='Caminho das pastas no storage'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='percents_completed',
            field=models.FloatField(default=0, verbose_name='Percentual Completo'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='start_backup_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 18, 14, 23, 36, 28366, tzinfo=utc), verbose_name='Hora de início do backup'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='storage_destiny_path',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Caminho das pastas a passar'),
        ),
        migrations.AlterField(
            model_name='backup',
            name='storage_ip',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Ip do storage'),
        ),
        migrations.AlterField(
            model_name='backuplog',
            name='log_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 18, 14, 23, 36, 29090, tzinfo=utc), verbose_name='Finish backup datetime'),
        ),
        migrations.AlterField(
            model_name='systeminfo',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 11, 18, 14, 23, 36, 27833, tzinfo=utc), verbose_name='Date'),
        ),
    ]