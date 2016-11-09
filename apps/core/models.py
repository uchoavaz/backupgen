
from django.db import models
from django.utils import timezone

STATUS_CHOICES = (
    (1, 'Rodando'),
    (2, 'Terminado'),
    (3, 'Alerta')

)


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
    success = models.BooleanField(verbose_name='Success ?', default=False)
    log_datetime = models.DateTimeField(
        'Finish backup datetime', default=timezone.now())
    class Meta:
        verbose_name = (u'Backup Log')
        verbose_name_plural = (u"Backups Log")
