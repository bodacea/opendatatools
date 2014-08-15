#!/usr/bin/env python
'''
Create spreadsheet filled with development indicators

Example use:
from fillIndicators import *
fillindicators("DRC")

Sara-Jayne Far2012
'''

import re
import xlrd
import xlwt
import time
import csv
import pycountry
import glob

'''
Get list of countries and country codes, either from file or from pycountries
library.

'''
def getcountries(code, filename):
    
    
    return(countries)


'''
Write list of countries to an excel workbook
'''
def countries_to_excel(country_list):
    
    #Set up output file
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Countries')
    ws.write(0,0, 'ISO Code')
    ws.write(0,1, 'Country Name')

    row = 1
    for country in country_list:
        ws.write(row,0, country.ISOalpha3)
        ws.write(row,1, country.ISOname)
        row += 1
    
    return(wb)


'''
Get indicators for a specific country
'''
def getindicators(iso3166code, csvdir="../../data/crisis_indicators_csv",
                  indexfile="", verbose=False):
    
    #Read in country codes
    try:
        country = pycountry.countries.get(alpha3=iso3166code)
        countryname = country.name
    except:
        if verbose:
            print("Country code "+str(iso3166code)+" not found. Exiting fillindicators.py")
            return

    if verbose:
        print("Creating indicator list for " + countryname)

    #Set dates of interest
    nyears = 5
    wantyears = []
    thisyear = time.gmtime().tm_year
    for yr in range(thisyear,thisyear-nyears,-1): #Latest year is furthest left
        wantyears += [str(yr)]

    #Read directory summary from xls file
    if indexfile == "":
        indexfile = "indicator_dbase_summary.xls"
    wbin = xlrd.open_workbook(indexfile)

    #sources
    sources = {}
    sourcefiles = {}
    sh_source = wbin.sheet_by_name(u'Datasources Used')
    for rownum in range(1,sh_source.nrows):
        row = sh_source.row_values(rownum)
        sourcecode = row[0]
        sourcename = row[1]
        sourcefile = row[5]
        sources[sourcecode] = sourcename
        sourcefiles[sourcefile] = sourcecode
        
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

    #Get data from csv files in directory
    data = {}
    lendir = len(csvdir) + 1
    csvfiles = glob.glob(csvdir + '/*.csv')
    for csvfile in csvfiles:
        match = re.findall('(.+?)_(.+?).csv', csvfile[lendir:])
        if match == []: #Ignore any files in the wrong form, e.g. iso3166.csv
            continue
        csvbase = match[0][0]
        csvyear = match[0][1]
        if csvyear in wantyears: #Only use data for the years we want
            sourcecode = sourcefiles[csvbase]
            if verbose:
                print("Input from file base " + csvbase + ", year " + csvyear)
            f = open(csvfile, 'rb')
            csvReader = csv.reader(f)
            headers = csvReader.next()
            fileinds = {}
            for col in range(0,len(headers)):
                if found[sourcecode].has_key(headers[col]):
                    fileinds[col] = found[sourcecode][headers[col]]
            #put file data into indicator data array as [indicator][source][year]
            for row in csvReader:
                if row[0] == iso3166code:
                    for col in fileinds.keys():
                        if len(row) > col:
                            if not(data.has_key(fileinds[col])):
                                data[fileinds[col]] = {}
                            if not(data[fileinds[col]].has_key(sourcecode)):
                                data[fileinds[col]][sourcecode] = {}
                            data[fileinds[col]][sourcecode][csvyear] = row[col]
            f.close()

    return indicators, sources, data, wantyears


#Populate array with indicator data
#Format is indicator name, units, 2012 value, 2011 value... 2008 value,
#latest year available, latest value, added by, data source, dataset,
#provenance - not all of these columns can be filled in at this point
def indicators_to_table(iso3166code, csvdir="../../data/crisis_indicators_csv",
                        indexfile="", verbose=False):

    #Get indicator data from files
    indicators, sources, data, datayears = getindicators(iso3166code, csvdir, 
                                                         indexfile, verbose)
    
    #Create indicator header row
    headers = ["Indicator", "Units"]
    for yr in datayears:
        headers += [yr + " value"]
    headers += ["Latest year available", "Latest value", "Added by"]
    headers += ["Data source", "Dataset", "Where *they* got this data from"]

    #Write each row of data; 1 row = 1 indicator from 1 datasource
    inddata = []
    for indcode in data.keys():
        for sourcecode in data[indcode].keys():
            rowdata = []
            rowdata += [indicators[indcode]]
            rowdata += ["---"]
            col = 2
            for yr in datayears:
                if data[indcode][sourcecode].has_key(yr):
                    rowdata += [data[indcode][sourcecode][yr]]
                else:
                    rowdata += ["---"]
                col = col+1
            rowdata += ["---"] #latest year available
            rowdata += ["---"] #latest value
            rowdata += ["Webpage scraper"] #Added by
            rowdata += [sources[sourcecode]] #data source
            rowdata += ["---"] #dataset #FIXIT - read this!
            rowdata += ["---"] #Provenance
            inddata += [rowdata]
            
    return headers, inddata


#Populate excel spreadsheet with indicator data
#Format is indicator name, units, 2012 value, 2011 value... 2008 value,
#latest year available, latest value, added by, data source, dataset,
#provenance - not all of these columns can be filled in at this point
def indicators_to_excel(iso3166code, csvdir="../../data/crisis_indicators_csv",
                        indexfile="", verbose=False):

    #Get indicator data from files
    indicators, sources, data, datayears = getindicators(iso3166code, csvdir, 
                                                         indexfile, verbose)
    
    wbout = xlwt.Workbook()
    sh1 = wbout.add_sheet("Indicators")

    #Create indicator header row
    headers = ["Indicator", "Units"]
    for yr in datayears:
        headers += [yr + " value"]
    headers += ["Latest year available", "Latest value", "Added by"]
    headers += ["Data source", "Dataset", "Where *they* got this data from"]
    for col in range(0,len(headers)):
        sh1.write(0,col,headers[col])

    #Write each row of data; 1 row = 1 indicator from 1 datasource
    row = 1
    for indcode in data.keys():
        for sourcecode in data[indcode].keys():
            sh1.write(row,0,indicators[indcode])
            sh1.write(row,1,"")
            col = 2
            for yr in datayears:
                if data[indcode][sourcecode].has_key(yr):
                    sh1.write(row,col,data[indcode][sourcecode][yr])
                else:
                    sh1.write(row,col,"---")
                col = col+1
            sh1.write(row,col,   "") #latest year available
            sh1.write(row,col+1, "") #latest value
            sh1.write(row,col+2, "Webpage scraper") #Added by
            sh1.write(row,col+3, sources[sourcecode]) #data source
            sh1.write(row,col+4, "") #dataset #FIXIT - read this!
            sh1.write(row,col+5, "") #Provenance
            row = row + 1
            
    return wbout


#Write excel spreadsheet of indicator values to a file
def write_indicator_excel_to_file(iso3166code, csvdir="../../data/crisis_indicators_csv",
                                  indexfile="", verbose=False):

    #Get indicators in excel workbook format
    wbout = indicators_to_excel(iso3166code, csvdir, indexfile, verbose)

    outfile = iso3166code + "indicators.xls"
    wbout.save(outfile)

    return

    
'''
Try filling in indicator summary data without using a database summary file

Sara-Jayne Farmer
2012
'''
def trywithoutfiles(iso3166code):
    #Create spreadsheet to hold indicators

    #Create list of required indicators - and map to known sources
    indicators = {}
    sources = {}

    indicator["below_poverty_line"] = {}
    indicator["below_poverty_line"]["meta"] = {}
    indicator["below_poverty_line"]["meta"]["title"] = "percentage of population living below poverty line (urban and rural)"

    sources["CIA"] = {}
    sources["CIA"]["meta"] = {}
    sources["CIA"]["meta"]["title"] = "Central Intelligence Agency World Factbook"
    sources["CIA"]["meta"]["URL"] = "https://www.cia.gov/library/publications/the-world-factbook/"
    sources["CIA"]["meta"]["API"] = ""
    sources["CIA"]["meta"]["localfile"] = "CIA_world_factbook_2012"
    sources["CIA"]["below_poverty_line"] = "2046"
    sources["CIA"]["land_cover"] = "xxxx"

    sources["GNA"] = {}
    sources["GNA"]["meta"] = {}
    sources["GNA"]["meta"]["title"] = "DG ECHO Global Needs Assessment"

    sources["FAOcountry"] = {}
    sources["FAOcountry"]["meta"] = {}
    sources["FAOcountry"]["meta"]["title"] = "FAO country profile"

    #Read data in from summary excelfile
    return()


