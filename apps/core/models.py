
from django.db import models
from django.utils import timezone

STATUS_CHOICES = (
    (1, 'Rodando'),
    (2, 'Terminado com sucesso'),
    (3, 'Terminado com erro')

)

class SystemInfo(models.Model):
    brand = models.CharField(verbose_name="Brand", max_length=50)
    designed_by = models.CharField(verbose_name="Designed by", max_length=50)
    version = models.CharField(verbose_name="Version", max_length=10)
    date = models.DateField(verbose_name="Date", default=timezone.now())

    class Meta:
        verbose_name = (u'System Information')
        verbose_name_plural = (u"Systems Informations")


class Backup(models.Model):
    name = models.CharField('Backup name', max_length=50)
    percents_completed = models.FloatField('Percents completed', default=0)
    start_backup_datetime = models.DateTimeField(
        'Start backup datetime', default=timezone.now())
    finish_backup_datetime = models.DateTimeField(
        'Finish backup datetime', null=True, blank=True)
    status = models.IntegerField('Status', choices=STATUS_CHOICES, default=1)

    class Meta:
        verbose_name = (u'Backup')
        verbose_name_plural = (u"Backups")

    def __str__(self):
        return self.name + " - " + str(self.start_backup_datetime)


class BackupLog(models.Model):
    backup = models.ForeignKey(
        Backup, verbose_name='backup', related_name='backup_log')
    log = models.TextField(verbose_name="Log")
    log_datetime = models.DateTimeField(
        'Finish backup datetime', default=timezone.now())
    status = models.IntegerField('Status', choices=STATUS_CHOICES, default=1)

    class Meta:
        verbose_name = (u'Backup Log')
        verbose_name_plural = (u"Backups Log")
