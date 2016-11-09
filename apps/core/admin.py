from django.contrib import admin
from .models import Backup
from .models import BackupLog


class BackupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'percents_completed',
        'status',
        'start_backup_datetime',
        'finish_backup_datetime'
    )

    search_fields = [
        'name',
        'percents_completed'
        'status',
        'start_backup_datetime',
        'finish_backup_datetime'
    ]


class BackupLogAdmin(admin.ModelAdmin):
    list_display = (
        'log',
        'success',
        'backup'
    )

    search_fields = [
        'log',
        'success',
    ]


admin.site.register(BackupLog, BackupLogAdmin)
admin.site.register(Backup, BackupAdmin)
