from django.db import models

class Country(models.Model):
    ISOalpha3 = models.CharField(max_length=3, primary_key=True)
    ISOname = models.CharField(max_length=200)
##    storedexcel = models.FileField(upload_to='countryindicators')
    def __unicode(self):
        return self.ISOname

class Indicator(models.Model):
    shortname = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    parentname = models.CharField(max_length=20)
    website = models.URLField()
    notes = models.TextField()
    def __unicode(self):
        return self.name

class Agency(models.Model):
    shortname = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=40)
    parentname = models.CharField(max_length=20)
    website = models.URLField()
    notes = models.TextField()
    scraped = models.BooleanField()
    
class Datasource(models.Model):
    shortname = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=40)
    notes = models.TextField()
    url = models.URLField()
    agency = models.CharField(max_length=20)
    dateadded = models.DateTimeField("date added")
    datechecked = models.DateTimeField("date last checked")
    scraper = models.BooleanField()
    localfile = models.CharField(max_length=40)
    def __unicode(self):
        return self.name

class CsvDatafile(models.Model):
    filename = models.CharField(max_length=400)
    pub_date = models.DateTimeField("date published")
    datasource = models.ForeignKey('Datasource')
    def __unicode(self):
        return self.filename

class foundIndicator(models.Model):
    indicator         = models.ForeignKey('Indicator')
    datasource        = models.ForeignKey('Datasource')
    csvfile           = models.ForeignKey('CsvDatafile')
    csvindname        = models.CharField(max_length=40)
    datasourceindname = models.CharField(max_length=20)
    datasourcedesc    = models.CharField(max_length=60)
    notes             = models.TextField()
##    def __unicode(self):
##        return self.indicator.shortname + " on " + self.datasource.shortname
    
