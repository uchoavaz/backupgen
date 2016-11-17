
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^backup_lookup$', views.backup_lookup, name='backup_lookup'),
    url(r'^backup_lookup/(?P<pk>\d+)/log$',
        views.backup_lookup_log, name='backup_lookup_log'),
    url(r'^gui_lookup$',
        views.get_lookup, name='gui_lookup'),
    url(r'^gui_home$',
        views.get_home, name='gui_home'),
    url(r'^gui_log_lookup$',
        views.get_log_lookup, name='gui_log_lookup')

]
