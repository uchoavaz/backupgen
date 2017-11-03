from django.contrib import admin
from .models import Backup
from .models import BackupLog
from .models import SystemInfo


class BackupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'percents_completed',
        'status',
        'start_backup_datetime',
        'finish_backup_datetime',
        'databases_passed',
        'databases_to_pass',
        'folders_passed',
        'database_storage_ip',
        'storage_ip',
        'path_folders_pass',
        'storage_destiny_path',
    )

    search_fields = [
        'name',
        'percents_completed',
        'status',
        'start_backup_datetime',
        'finish_backup_datetime',
        'databases_passed',
        'databases_to_pass',
        'folders_passed',
        'database_storage_ip',
        'storage_ip',
        'path_folders_pass',
        'storage_destiny_path',
    ]


class BackupLogAdmin(admin.ModelAdmin):
    list_display = (
        'log',
        'status',
        'backup'
    )

    search_fields = [
        'log',
        'status',
    ]


class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('brand', 'designed_by', 'version', 'date')


admin.site.register(SystemInfo, SystemInfoAdmin)
admin.site.register(BackupLog, BackupLogAdmin)
admin.site.register(Backup, BackupAdmin)
