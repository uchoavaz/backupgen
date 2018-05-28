
from django.db import models
from django.utils import timezone

STATUS_CHOICES = (
    (1, 'Rodando'),
    (2, 'Terminado com sucesso'),
    (3, 'Alerta'),
    (4, 'Erro')
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
    name = models.CharField('Nome do backup', max_length=50)
    percents_completed = models.FloatField('Percentual Completo', default=0)
    start_backup_datetime = models.DateTimeField(
        'Hora de início do backup', default=timezone.now())
    finish_backup_datetime = models.DateTimeField(
        'Hora de fim do backuo', null=True, blank=True)
    databases_passed = models.TextField('Bancos passados', null=True, blank=True)
    databases_to_pass = models.TextField('Bancos a passar', null=True, blank=True)
    database_storage_ip = models.CharField(
        'Ip do banco e das pastas', max_length=15, null=True, blank=True)
    storage_ip = models.CharField(
        'Ip do storage', max_length=15, null=True, blank=True)
    path_folders_pass = models.TextField(
        'Caminho das pastas no storage', null=True, blank=True)
    storage_destiny_path = models.TextField(
        'Caminho no storage dos backups', default='', null=True, blank=True)
    folders_passed = models.TextField(
        'Pastas passadas para o storage', default='', null=True, blank=True)
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
