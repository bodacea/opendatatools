#!/usr/bin/env python
# -*- coding: cp1252 -*-

#This program either:
# * searches the pycountries database for a country name
#   returns the ISO-3166 3-digit country code for that country, or "---" if it can't
#   find the country
#   Also returns the ISO-3166 name for the country
# * Searches the data.un.org list of UN region and country codes, and returns the UN
#   3-digit code if found, "---" if not
#
#Example use:
#
#c = CleanData()
#c.MakeIndexHistogram("undata2012-Apr-09-22-09-23")
#c.CheckCountriesInFile("uncountriesin.txt")
#
#Sara-Jayne Farmer
#2012

import collections
import csv
import glob
import os
import pycountry
import re
import string
import xlrd


#======================================================================================
#Clean up data in arrays where the first column in each array is an index
# - usually country, sometimes region or economic status
#And we expect the files to also contain footnotes
#
#Sara-Jayne Farmer
#2012
#======================================================================================
class CleanUNDataOrg:
    Name = "CleanUNDataOrg"
    
    #Remove footnotes, notes and headers from un files
    def remove_un_footnotes(self, undir, mart, dataset):
        print("Removing un footnotes into separate file")
        

    #Clean data downloaded from data.un.org
    def CleanUndataDirectory(self, undir):

        #Create clean directory, if it doesn't already exist
        #(Process in the current directory)
        rawdir = undir + "/raw"
        cleandir = undir + "/clean"
        if os.path.isdir(cleandir) == False:
            os.mkdir(cleandir)

        #Open raw directory, and process each file
        datafiles = os.listdata(rawdir)
        for datafile in datafiles:

            print("Cleaning UN datafile " + datafile)

            #Get file information from its filename
            #Expects filename to be in form "mart_storeid_grabdate.extn"
            dotpos = datafile.rfind(".")
            underscores = [m.start() for m in re.finditer("_", datafile[:dotpos])]
            extn = datafile[dotpos+1:]
            mart = datafile[:underscores[0]]
            storeid = datafile[uderscores[0]+1:underscores[1]]
            grabdate = datafile[uderscores[1]+1:dotpos]

            #Preprocess: excel files (15, 16 etc)
            if (extn == "xls"):
                
                CleanUnExcelFile(mart, datafile)

            elif(extn == "csv"):
                print("csv found")
                #Preprocess: IFS: Swap columns (OID, Country)

                #No major quirks: CLINO, COMTRADE, EDATA, ENV, FAO, GENDERSTAT, GHG, KS, ITU,  
                #LABORSTA, MGD, POP, POPDIV, SNA, SNAAMA, UNAIDS, UNESCO, UNIDO, UNODC, WHO.

                #Clino:
                #- Axes are station name (not country) and label. Station name is col B.

                #Comtrade:
                #- 3d table in 2d form
                #  Axes are country, year, label
                

            else:
                print("unknown file type: " + extn + " no cleaning file " + datafile)
                return()


            #Clean up headings

            #Strip off footnotes into separate _notes files - add filenames to index file

            #Check lhs index, and split out into separate files for countries, regions, etc
            #as _country _region _other - add filenames to index file
            #SOWC and WDI both have countries and regions mixed; others are just countries


    #Find country-specific data in data.un.org
    def FindInUndataDirectory(self, undir, index):

        #Create clean directory, if it doesn't already exist
        #(Process in the current directory)
        rawdir = undir + "/raw"

        #Open raw directory, and process each file
        datafiles = os.listdata(rawdir)
        for datafile in datafiles:

            print("Cleaning UN datafile " + datafile)

            #Get file information from its filename
            #Expects filename to be in form "mart_storeid_grabdate.extn"
            dotpos = datafile.rfind(".")
            underscores = [m.start() for m in re.finditer("_", datafile[:dotpos])]
            extn = datafile[dotpos+1:]
            mart = datafile[:underscores[0]]
            storeid = datafile[uderscores[0]+1:underscores[1]]
            grabdate = datafile[uderscores[1]+1:dotpos]

            #Preprocess: excel files (15, 16 etc)
            if (extn == "xls"):
                
                CleanUnExcelFile(mart, datafile)

            elif(extn == "csv"):
                print("csv found")
                #Preprocess: IFS: Swap columns (OID, Country)

                #No major quirks: CLINO, COMTRADE, EDATA, ENV, FAO, GENDERSTAT, GHG, KS, ITU,  
                #LABORSTA, MGD, POP, POPDIV, SNA, SNAAMA, UNAIDS, UNESCO, UNIDO, UNODC, WHO.

                #Clino:
                #- Axes are station name (not country) and label. Station name is col B.

                #Comtrade:
                #- 3d table in 2d form
                #  Axes are country, year, label
                

            else:
                print("unknown file type: " + extn + " no cleaning file " + datafile)
                return()


            #Clean up headings

            #Strip off footnotes into separate _notes files - add filenames to index file

            #Check lhs index, and split out into separate files for countries, regions, etc
            #as _country _region _other - add filenames to index file
            #SOWC and WDI both have countries and regions mixed; others are just countries

        



