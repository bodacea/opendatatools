from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^indicators/', include('indicators.urls')),
    url(r'^admin/',  include(admin.site.urls)),
)
