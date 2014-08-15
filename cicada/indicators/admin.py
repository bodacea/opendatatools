from django.contrib import admin
from models import Country
from models import Indicator
from models import CsvDatafile

admin.site.register(Country)
admin.site.register(Indicator)
admin.site.register(CsvDatafile)
