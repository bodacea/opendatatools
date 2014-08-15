# -*- coding: utf_8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.encoding import smart_unicode
import csv
import xlwt
from fillIndicators import *
from bdt.cicada.models import Agency,Country

def index(request):
    country_list = Country.objects.all().order_by('ISOname')
    return render_to_response('cicada/index.html',
                              {'country_list': country_list},
                              context_instance=RequestContext(request))
##    return HttpResponse("Hello, world. You're at the cicada index.")

def generate_countries_excel_old(request):
    yearnum = 2013
    response = render_to_response("spreadsheet.html", {
        'names': ['aa', 'bb', 'cc'],
        'codes': ['11', '22', '33'],
    })
    filename = "countries%s.xls" % (yearnum)
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'

    return response

def country_list_excel(request):

    #Set up output file
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=countrylist.xls'    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Countries')
    ws.write(0,0, 'ISO Code')
    ws.write(0,1, 'Country Name')

    country_list = Country.objects.all().order_by('ISOname')
    row = 1
    for country in country_list:
        ws.write(row,0, country.ISOalpha3)
        ws.write(row,1, country.ISOname)
        row += 1

    wb.save(response)
    return response

#Get html table containing known indicators for a given country code
def country(request, countrycode):

    indheaders, indicators = indicators_to_table(countrycode, "static/indicator_csvs")
    countrydata = {}
    countrydata['code'] = countrycode
    countrydata['headers'] = indheaders
    countrydata['indicators'] = indicators
    return render_to_response('cicada/indicators.html',
                              {'countrydata': countrydata},
                              context_instance=RequestContext(request))


#Get excel file containing known indicators for a given country code
def country_excel(request, countrycode):

    #Set Excel headers, including output filename
    filename = countrycode + '_indicators.xls'
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename='+filename

    #Get and save Excel file contents
    wbout = indicators_to_excel(countrycode, "static/indicator_csvs")
    wbout.save(response)
    
    return response


#Load list of countries into database
def load_countries(request, indexfile=""):
    if indexfile == "":
        indexfile = "cicada_iso3166codes.csv"

    fin = open(indexfile, 'rb')
    csvin = csv.reader(fin)
    headers = csvin.next()
    for row in csvin:
        print(row[0] + ":" + row[1])
        print(type(row[1]))
        newcountry = Country(ISOalpha3=row[0].decode('latin-1'),
                             ISOname=row[1].decode('latin-1'))
        newcountry.save()
    return HttpResponse("Country details loaded from file "+ indexfile)


def agencies(request):
    agency_list = Agency.objects.all().order_by('shortname')
    return render_to_response('cicada/agencies.html',
                              {'agency_list': agency_list},
                              context_instance=RequestContext(request))


#Open excel spreadsheet containing summary of crisis indicators,
#and add its contents to the correct Django models
def load_agency_summaries(request, indexfile=""):

    #Open summary excelfile
    wbin = xlrd.open_workbook(indexfile)

    #Agencies
    sh_source = wbin.sheet_by_name(u'Agencies')
    for rownum in range(1,sh_source.nrows):
        row = sh_source.row_values(rownum)
        shortname  = row[0]
        fullname   = row[1]
        parentname = row[2]
        website    = row[3]
        newagency = Agency(shortname=shortname, name=fullname, parentname=parentname,
                           website=website, notes="", scraped=scraped)
        newagency.save()
    return HttpResponse("Agency details loaded from file.")


#Open excel spreadsheet containing summary of crisis indicators,
#and add its contents to the correct Django models
def load_indicator_summaries(request, indexfile=""):

    #Open summary excelfile
    wbin = xlrd.open_workbook(indexfile)

    #Agencies
    sh_source = wbin.sheet_by_name(u'Agencies')
    for rownum in range(1,sh_source.nrows):
        row = sh_source.row_values(rownum)
        shortname  = row[0]
        fullname   = row[1]
        parentname = row[2]
        website    = row[3]
        newagency = Agency(shortname=shortname, name=fullname, parentname=parentname,
                           website=website, notes="")
        newagency.save()
    
    #Datasources
    datasources = {}
    sourcefiles = {}
    sh_source = wbin.sheet_by_name(u'Datasources Used')
    for rownum in range(1,sh_source.nrows):
        row = sh_source.row_values(rownum)
        sourcecode = row[0]
        sourcename = row[1]
        sourcefile = row[5]
        datasources[sourcecode] = sourcename
        sourcefiles[sourcefile] = sourcecode
        
    sh_source = wbin.sheet_by_name(u'Suggested Sources')
    for rownum in range(1,sh_source.nrows):
        row = sh_source.row_values(rownum)
        sourcecode = row[0]
    
        
    #Indicators
    indicators = {}
    sh_ind = wbin.sheet_by_name(u'Indicators Needed')
    for rownum in range(1,sh_ind.nrows):
        row = sh_ind.row_values(rownum)
        indcode = row[0]
        indname = row[1]
        indicators[indcode] = indname

    #Indicators in sources
    found = {}
    sh_found = wbin.sheet_by_name(u'Indicators Found')
    for rownum in range(1,sh_found.nrows):
        row = sh_found.row_values(rownum)
        sourcecode = row[0]
        indcode = row[1]
        csvheading = row[4]
        #Only process indicators that we have data for
        if not(csvheading == ""):
            if not(found.has_key(sourcecode)):
                found[sourcecode] = {}
            found[sourcecode][csvheading] = indcode
    
    sh_found = wbin.sheet_by_name(u'Indicators NOT found')
    for rownum in range(1,sh_found.nrows):
        row = sh_found.row_values(rownum)
        sourcecode = row[0]
        indcode = row[1]
        csvheading = row[4]

    return HttpResponse("Indicator details loaded from file.")
