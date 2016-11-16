
from django import template
from apps.core.models import Backup
from django.utils import timezone
import math


register = template.Library()


@register.assignment_tag
def get_count_bkps(backup_name):
    count = Backup.objects.filter(name=backup_name).count()
    return count


@register.assignment_tag
def get_last_status_display(backup_name):
    bkp = Backup.objects.filter(name=backup_name)
    bkp = bkp.order_by('start_backup_datetime')
    return bkp.last().get_status_display()


@register.assignment_tag
def get_last_status(backup_name):
    bkp = Backup.objects.filter(name=backup_name)
    bkp = bkp.order_by('start_backup_datetime')
    return bkp.last().get_status_display().replace(' ', '_')


@register.assignment_tag
def get_last_start_date_bkp(backup_name):
    bkp = Backup.objects.filter(name=backup_name)
    bkp = bkp.order_by('start_backup_datetime')
    date = timezone.localtime(bkp.last().start_backup_datetime)
    return date.strftime('%d/%m/%Y às %H:%M Hrs.')


@register.assignment_tag
def get_last_finish_date_bkp(backup_name):
    try:
        bkp = Backup.objects.filter(name=backup_name)
        bkp = bkp.order_by('start_backup_datetime')
        date = timezone.localtime(bkp.last().finish_backup_datetime)
        return date.strftime('%d/%m/%Y às %H:%M Hrs.')

    except AttributeError:
        return '-'


@register.assignment_tag
def get_last_update(backup_name):
    bkp = Backup.objects.filter(name=backup_name).last()
    if bkp.finish_backup_datetime is None:
        start_date = bkp.start_backup_datetime
        time_now = timezone.now()
        minutes = (timezone.localtime(time_now) - timezone.localtime(
            start_date)).seconds / 60

        minutes_floor = math.floor(minutes)
        return 'Há ' + str(minutes_floor) + ' minutos'
    else:
        return '-'
