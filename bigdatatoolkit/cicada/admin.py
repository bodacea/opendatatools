from django.contrib import admin
from bdt.cicada.models import Country
from bdt.cicada.models import Indicator
from bdt.cicada.models import CsvDatafile

admin.site.register(Country)
admin.site.register(Indicator)
admin.site.register(CsvDatafile)
