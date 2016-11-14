
from django.conf.urls import url
from apps.accounts import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^password$', views.password, name='password')
]
