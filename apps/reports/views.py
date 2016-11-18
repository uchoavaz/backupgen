
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.http import HttpResponse
from apps.core.models import Backup
from django.contrib import messages
from datetime import datetime
import csv


def correct_date_get_request(request, start_date, end_date):
    if start_date != '':
        try:
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        except (ValueError, UnicodeEncodeError):
            msg = 'Data início incorreta'
            raise Exception(msg)
        except TypeError:
            start_date = ''

    if end_date != '':
        try:
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
        except (ValueError, UnicodeEncodeError):
            msg = 'Data fim incorreta'

            end_date = ''
            raise Exception(msg)
        except TypeError:
            end_date = ''
    if start_date != '' and end_date != '' \
            and (end_date - start_date).days < 0:
            msg = 'Data fim maior que a data início'
            raise Exception(msg)

    return {'start_date': start_date, 'end_date': end_date}


class ReportView(TemplateView):
    template_name = 'report.html'

    def generate_csv(self, file_name, date_str, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="{0}_backup_report{1}.csv"'.format(
                file_name, date_str)

        writer = csv.writer(response, delimiter=';')
        header = [
            Backup._meta.get_field("name").verbose_name.title(),
            Backup._meta.get_field(
                "start_backup_datetime").verbose_name.title(),
            Backup._meta.get_field(
                "finish_backup_datetime").verbose_name.title(),
            Backup._meta.get_field("status").verbose_name.title(),
            Backup._meta.get_field("database_storage_ip").verbose_name.title(),
            Backup._meta.get_field("databases_passed").verbose_name.title(),
            Backup._meta.get_field("folders_passed").verbose_name.title(),
            Backup._meta.get_field("storage_ip").verbose_name.title(),
            Backup._meta.get_field(
                "storage_destiny_path").verbose_name.title(),
            Backup._meta.get_field("path_folders_pass").verbose_name.title()

        ]
        writer.writerow(header)
        for line in queryset:
            try:
                finish_date = line.finish_backup_datetime.strftime(
                    '%d-%m-%Y %H:%M')
            except AttributeError:
                finish_date = 'Não Concluido'
            writer.writerow([
                line.name,
                line.start_backup_datetime.strftime('%d-%m-%Y %H:%M'),
                finish_date,
                line.get_status_display(),
                line.database_storage_ip,
                line.databases_passed,
                line.folders_passed,
                line.storage_ip,
                line.storage_destiny_path,
                line.path_folders_pass
            ])
        return response


    def get(self, request, *args, **kwargs):
        try:
            if self.request.GET:
                bkp_name = self.request.GET.get('backup_name')
                start_date = self.request.GET.get('start_date')
                end_date = self.request.GET.get('end_date')

                queryset = Backup.objects.filter(name=bkp_name)
                get = correct_date_get_request(
                    self.request, start_date, end_date)
                start_date = get['start_date']
                end_date = get['end_date']

                start_date_str = ''
                end_date_str = ''
                date_str = ''
                if start_date != '':
                    queryset = queryset.filter(
                        start_backup_datetime__gte=start_date)
                    start_date_str = start_date.strftime('%d_%m_%Y')
                if end_date != '':
                    queryset = queryset.filter(
                        start_backup_datetime__lte=end_date)
                    end_date_str = end_date.strftime('%d_%m_%Y')

                if start_date_str != '' or end_date_str != '':
                    date_str = "_" + start_date_str + "__to__" + end_date_str

                queryset = queryset.order_by('start_backup_datetime')
                return self.generate_csv(
                    queryset[0].name, date_str, queryset)

        except (ValueError, ObjectDoesNotExist):
            messages.error(self.request, "Backup não existe")
        except TypeError:
            messages.error(
                self.request, 'Insira um Local')
        except IndexError:
            messages.error(
                self.request, 'Não existe backups neste intervalo de data')
        except Exception as err:
            messages.error(self.request, err)
        return super(ReportView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['backups'] = Backup.objects.all().distinct('name')
        return context

report = ReportView.as_view()
