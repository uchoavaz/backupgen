
from django import template
from apps.core.models import Backup
from apps.core.models import BackupLog
from django.utils import timezone
import math


register = template.Library()


@register.assignment_tag
def last_update(bkp_pk):
    bkp = Backup.objects.get(pk=bkp_pk)
    if bkp.finish_backup_datetime is None:
        start_date = bkp.start_backup_datetime
        time_now = timezone.now()
        minutes = (timezone.localtime(time_now) - timezone.localtime(
            start_date)).seconds / 60

        minutes_floor = math.floor(minutes)
        return 'Há ' + str(minutes_floor) + ' minutos'
    else:
        return '-'


@register.assignment_tag
def get_finish_date(bkp_pk):
    bkp = Backup.objects.get(pk=bkp_pk)
    if bkp.finish_backup_datetime is None:
        return '-'
    else:
        date = timezone.localtime(bkp.finish_backup_datetime)
        return date.strftime('%d/%m/%Y às %H:%M Hrs.')


@register.assignment_tag
def get_start_date(bkp_pk):
    bkp = Backup.objects.get(pk=bkp_pk)
    date = timezone.localtime(bkp.start_backup_datetime)
    return date.strftime('%d/%m/%Y às %H:%M Hrs.')


@register.assignment_tag
def get_log_status(bkp_pk):
    status_log = BackupLog.objects.get(pk=bkp_pk).get_status_display()
    status_log = status_log.replace(' ','_')
    return status_log


@register.assignment_tag
def get_status_display(bkp_pk):
    status_display = Backup.objects.get(pk=bkp_pk).get_status_display()
    status_display = status_display.replace(' ', '_')
    return status_display


@register.assignment_tag
def transform_percentage(number):
    percentage = str(number).replace(',', '.')
    return percentage
