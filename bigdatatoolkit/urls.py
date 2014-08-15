from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^cicada/', include('cicada.urls')),
    url(r'^volta/', include('volta.urls')),
    url(r'^admin/',  include(admin.site.urls)),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
