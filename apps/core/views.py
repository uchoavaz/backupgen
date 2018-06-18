
import math
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from apps.core.models import Backup
from apps.core.models import BackupLog
from apps.core.models import SystemInfo
from django.utils import timezone
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.core.models import STATUS_CHOICES


class SystemInfoView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("accounts:login")

    def get_context_data(self, **kwargs):
        context = super(SystemInfoView, self).get_context_data(**kwargs)
        system_info = SystemInfo.objects.all()
        context['system_info'] = True
        context['request'] = self.request
        try:
            last_system_info = system_info.last()
            context['brand'] = last_system_info.brand
            context['designed_by'] = last_system_info.designed_by
            context['version'] = last_system_info.version
        except AssertionError:
            context['brand'] = ''
            context['designed_by'] = ''
            context['version'] = ''
            context['system_info'] = False

        return context


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
        system_info = SystemInfo.objects.all()
        context['system_info'] = True
        context['request'] = self.request
        try:
            last_system_info = system_info.last()
            context['brand'] = last_system_info.brand
            context['designed_by'] = last_system_info.designed_by
            context['version'] = last_system_info.version
        except AssertionError:
            context['brand'] = ''
            context['designed_by'] = ''
            context['version'] = ''
            context['system_info'] = False
        return context


class BackupLookupView(SystemInfoView, ListView):
    template_name = 'backup_lookup.html'
    model = Backup
    paginated_by = 10

    def get_context_data(self, **kwargs):
        context = super(BackupLookupView, self).get_context_data(**kwargs)
        bkp_name = self.request.GET.get('backup_name')
        search_request = self.request.GET.get('search')
        context['backup_name'] = bkp_name
        link_home = reverse('core:home')
        link_backup_lookup = reverse(
            'core:backup_lookup') + '?backup_name={0}'.format(bkp_name)
        context['links'] = [
            ['Backups disponíveis', link_home], [bkp_name, link_backup_lookup]
        ]
        context['link_backup_lookup'] = link_backup_lookup
        pages_list = self.get_pages_list()
        page = self.get_page()
        context['page'] = page
        context['paginated_by'] = self.paginated_by
        context['pagination'] = self.get_actual_page_in_list(pages_list, page)
        if search_request is None:
            search_request = ''
        context['search_field'] = search_request
        return context

    def get_queryset(self):
        queryset = super(BackupLookupView, self).get_queryset()
        field = self.request.GET.get('search')
        backup_name = self.request.GET.get('backup_name')
        page = self.get_page()
        queryset = queryset.filter(
            name=backup_name).order_by('-start_backup_datetime')
        queryset = self.search_status(queryset, field)
        queryset = self.search_initial_datetime(queryset, field, self.model)
        queryset = self.search_finish_datetime(queryset, field, self.model)
        minimum = (page - 1) * self.paginated_by
        maximum = page * self.paginated_by

        queryset = queryset[minimum:maximum]
        return queryset

    def search_finish_datetime(self, queryset, field, model):
        if field is not None and field != '':

            try:
                field = int(field)

                if not queryset:
                    queryset = model.objects.filter(
                        finish_backup_datetime__year=field)
                if not queryset:
                    queryset = model.objects.filter(
                        finish_backup_datetime__month=field)
                if not queryset:
                    queryset = model.objects.filter(
                        finish_backup_datetime__day=field)
            except ValueError:
                pass
        return queryset

    def search_initial_datetime(self, queryset, field, model):
        if field is not None and field != '':

            try:
                field = int(field)

                if not queryset:
                    queryset = model.objects.filter(
                        start_backup_datetime__year=field)
                if not queryset:
                    queryset = model.objects.filter(
                        start_backup_datetime__month=field)
                if not queryset:
                    queryset = model.objects.filter(
                        start_backup_datetime__day=field)
            except ValueError:
                pass
        return queryset

    def search_status(self, queryset, field):

        if field is not None and field != '':
                status = self.get_status(field, STATUS_CHOICES)
                print (status)
                queryset = queryset.filter(status=status)
        return queryset

    def get_page(self):
        page = None
        try:
            page = int(self.request.GET.get('page'))
        except TypeError:
            page = 1

        return page

    def get_status(self, name, choices):
        for choice in choices:
            if name.lower() in choice[1].lower():
                return choice[0]
        return 0

    def get_pages_list(self):
        backup_name = self.request.GET.get('backup_name')
        queryset = self.model.objects.filter(name=backup_name)
        field = self.request.GET.get('search')
        queryset = self.search_status(queryset, field)
        queryset = self.search_initial_datetime(queryset, field, self.model)
        queryset = self.search_finish_datetime(queryset, field, self.model)
        pages = math.ceil(queryset.count() / self.paginated_by)
        range_list = range(1, (pages + 1))
        if len(range_list) == 0:
            range_list = range(1, 2)
        return range_list

    def get_actual_page_in_list(self, pages_list, actual_page):
        pagination = []
        for page in pages_list:
            t = []
            if actual_page == page:
                t = ['active', page]
            else:
                t = ['', page]
            pagination.append(t)
        return pagination


class BackupLookupLogView(SystemInfoView, ListView):
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
        queryset = queryset.filter(backup__pk=backup_pk).order_by(
            'log_datetime')
        return queryset


def get_lookup(request):
    bkp_name = request.GET.get('backup_name')
    page = int(request.GET.get('page'))
    search = request.GET.get('search')
    print (search)

    paginated_by = int(request.GET.get('paginated_by'))
    queryset = Backup.objects.filter(
        name=bkp_name).order_by('-start_backup_datetime')

    if search is not None and search != '':
            status = get_status(search, STATUS_CHOICES)
            queryset = queryset.filter(status=status)

    if search is not None and search != '':

        try:
            search = int(search)

            if not queryset:
                queryset = Backup.objects.filter(
                    start_backup_datetime__year=search)
            if not queryset:
                queryset = Backup.objects.filter(
                    start_backup_datetime__month=search)
            if not queryset:
                queryset = Backup.objects.filter(
                    start_backup_datetime__day=search)
        except ValueError:
            pass
    if search is not None and search != '':

        try:
            search = int(search)

            if not queryset:
                queryset = Backup.objects.filter(
                    finish_backup_datetime__year=search)
            if not queryset:
                queryset = Backup.objects.filter(
                    finish_backup_datetime__month=search)
            if not queryset:
                queryset = Backup.objects.filter(
                    finish_backup_datetime__day=search)
        except ValueError:
            pass
    minimum = (page - 1) * paginated_by
    maximum = page * paginated_by

    queryset = queryset[minimum:maximum]
    template = 'tr_body_lookup.html'
    return render_to_response(
        template,
        {'object_list': queryset},
        context_instance=RequestContext(request)
    )


def get_status(name, choices):
    for choice in choices:
        if name.lower() in choice[1].lower():
            return choice[0]
    return 0


def get_home(request):
    bkp = Backup.objects.all().values('name').distinct()
    template = 'tr_body_home.html'
    return render_to_response(
        template,
        {'object_list': bkp},
        context_instance=RequestContext(request)
    )


def get_log_lookup(request):
    backup_pk = request.GET.get('backup_pk')
    bkp = Backup.objects.get(pk=backup_pk)
    finish_date = bkp.finish_backup_datetime
    try:
        finish_date = timezone.localtime(finish_date).strftime(
            '%d/%m/%Y às %H:%M')
    except AttributeError:
        finish_date = 'Não concluído'
    start_date = timezone.localtime(bkp.start_backup_datetime).strftime(
        '%d/%m/%Y às %H:%M')
    bkp_log = BackupLog.objects.filter(backup__pk=backup_pk).order_by(
        'log_datetime')
    template = 'body_log_lookup.html'
    return render_to_response(
        template,
        {
            'object_list': bkp_log,
            'finish_date': finish_date,
            'start_date': start_date,
            'backup_info': bkp
        },
        context_instance=RequestContext(request)
    )

backup_lookup_log = BackupLookupLogView.as_view()
backup_lookup = BackupLookupView.as_view()
home = HomeView.as_view()
