
from django.views.generic import TemplateView
from apps.core.models import Backup
from django.contrib import messages
from datetime import datetime



def correct_date_get_request(request, start_date, end_date):
    if start_date != '':
        try:
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        except (ValueError, UnicodeEncodeError):
            messages.error(
                request,
                u'Data início incorreta')
            start_date = ''
        except TypeError:
            start_date = ''

    if end_date != '':
        try:
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
        except (ValueError, UnicodeEncodeError):
            messages.error(
                request, 'Data fim incorreta')
            end_date = ''
        except TypeError:
            end_date = ''
    if start_date != '' and end_date != '' \
            and (end_date - start_date).days < 0:
            messages.error(
                request, 'Data fim maior que a data início')

    return {'start_date': start_date, 'end_date': end_date}

class ReportView(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        get = correct_date_get_request(self.request, start_date, end_date)
        return super(ReportView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['backups'] = Backup.objects.all().distinct('name')
        return context

report = ReportView.as_view()
