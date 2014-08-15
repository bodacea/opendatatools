from django.conf.urls import patterns, url

from indicators import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^country/(?P<countrycode>\w{3})/$', views.country, name='country'),
    url(r'^country/excel/(?P<countrycode>\w{3})/$', views.country_excel, name='country_excel'),
    url(r'^countries/excel$', views.country_list_excel, name='countries_excel'),
    url(r'^countries/load$', views.load_countries, name='countries_load'),
    url(r'^agencies$', views.agencies, name='agencies'),
    url(r'^agencies/load/(?P<indexfile>[^#?]*?)$', views.load_agencies, name='load_agencies'),
    url(r'^loadsummaryfile/(?P<indexfile>.*)$', views.load_indicator_spreadsheet, name='summaryfile_load'),
)
