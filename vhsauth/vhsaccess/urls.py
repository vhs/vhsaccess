from django.conf.urls import patterns, url

from vhsaccess import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^authorize/(?P<code>\w+)/$', views.authorize, name='authorize')
)
