from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^backup_lookup$', views.backup_lookup, name='backup_lookup'),
    url(r'^backup_lookup/(?P<pk>\d+)/log$',
        views.backup_lookup_log, name='backup_lookup_log'),


]
