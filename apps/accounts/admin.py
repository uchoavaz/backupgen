from django.contrib import admin
from apps.accounts.models import BackupUser


class BackupUserAdmin(admin.ModelAdmin):
    list_filter = ['email']
    list_display = (
        'email', 'is_staff',
        'is_active', 'is_superuser')


admin.site.register(BackupUser, BackupUserAdmin)