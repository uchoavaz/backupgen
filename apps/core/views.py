
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from apps.core.models import Backup
from apps.core.models import BackupLog
from django.utils import timezone


class HomeView(ListView):
    template_name = "home.html"
    model = Backup

    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        queryset = queryset.values('name').distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        link_home = reverse('core:home')
        context['links'] = [['Backups disponíveis', link_home]]
        return context


class BackupLookupView(ListView):
    template_name = 'backup_lookup.html'
    model = Backup

    def get_context_data(self, **kwargs):
        context = super(BackupLookupView, self).get_context_data(**kwargs)
        bkp_name = self.request.GET.get('backup_name')
        context['backup_name'] = bkp_name
        link_home = reverse('core:home')
        link_backup_lookup = reverse(
            'core:backup_lookup') + '?backup_name={0}'.format(bkp_name)
        context['links'] = [
            ['Backups disponíveis', link_home], [bkp_name, link_backup_lookup]
        ]
        return context

    def get_queryset(self):
        queryset = super(BackupLookupView, self).get_queryset()
        backup_name = self.request.GET.get('backup_name')
        queryset = queryset.filter(name=backup_name)
        return queryset


class BackupLookupLogView(ListView):
    template_name = 'bkp_lookup_log.html'
    model = BackupLog

    def get_context_data(self, **kwargs):
        context = super(BackupLookupLogView, self).get_context_data(**kwargs)
        context['backup_info'] = Backup.objects.get(pk=self.kwargs['pk'])
        backup = Backup.objects.get(pk=self.kwargs['pk'])
        start_date = backup.start_backup_datetime
        finish_date = backup.finish_backup_datetime
        context['start_date'] = timezone.localtime(start_date).strftime(
            '%d/%m/%Y às %H:%M')
        try:
            context['finish_date'] = timezone.localtime(finish_date).strftime(
                '%d/%m/%Y às %H:%M')
        except AttributeError:
            context['finish_date'] = 'Não concluído'
        link_home = reverse('core:home')
        bkp_name = Backup.objects.get(pk=self.kwargs['pk']).name
        link_backup_lookup = reverse(
            'core:backup_lookup') + '?backup_name={0}'.format(bkp_name)
        link_backup_lookup_log = reverse(
            'core:backup_lookup_log', kwargs={'pk': self.kwargs['pk']})
        context['links'] = [
            ['Backups disponíveis', link_home],
            [bkp_name, link_backup_lookup],
            ['Visualizar Log', link_backup_lookup_log]
        ]
        return context

    def get_queryset(self):
        queryset = super(BackupLookupLogView, self).get_queryset()
        backup_pk = self.kwargs['pk']
        queryset = queryset.filter(backup__pk=backup_pk)
        return queryset


backup_lookup_log = BackupLookupLogView.as_view()
backup_lookup = BackupLookupView.as_view()
home = HomeView.as_view()
