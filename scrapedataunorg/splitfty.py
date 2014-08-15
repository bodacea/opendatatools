#!/usr/bin/env python
# -*- coding: cp1252 -*-

#Convert csv spreadsheet with 2 columns of countries and 1 year into a
#set of excel spreadsheets, with one worksheet per year
#
#Design: store data as dictionary of years; each containing dictionary of
#from-countries containing dictionary of to-countries pointing to data values.
#Vt values are from country (column 0); Hz values are to country (column 1);
#Picks out columns 3 and 5. (but could also do columns 4 and 6).
#Do: create dictionaries, output to excel: 1 file per dataset,
#1 worksheet per year, with headings that are ISO3166 codes.
#
#Example use:
#from splitfty import *
#splitfromtoyear("cleaned_ISO3166_2012-Jul-13-09-21-39/Table with data on Refugees - 1975-1999.csv")

import csv
import xlwt

#Convert table with rows containing from-country, to-country, year and values
#into spreadsheets containing one worksheet per year, from-country as index
#and to-country as column headings
#
#Sara-Jayne Farmer
#2012
def splitfromtoyear(infile):
    
    tocountries = {} #Array of dictionary of "to" countries
    yeardatacol = {} #Array of dictionaries of data by year
    for i in range(0,4):
        yeardatacol[i] = {}
        tocountries[i] = {}
    
    #open csv file
    fin = open(infile, "rb")
    csvin = csv.reader(fin)
    #Grab the column headers for use in the output excel files
    headers = csvin.next()
    tablelabels = ["","","",""]
    for i in range(3,len(headers)):
        tablelabels[i-3] = headers[i]
    
    #fill up the dictionaries
    ccol = ["0","0","0","0"]
    for row in csvin:
        
        #Ignore empty rows
        if len(row) == 0:
            continue
        
        cfrom = row[0]
        cto = row[1]
        cyear = row[2]
        #NB some input rows have 3 values; others have 4
        for i in range(3,len(row)):
            ccol[i-3] = row[i]
        
        for col in range(0,len(row)-3):
            
            #Ignore empty cells
            if ccol[col] == "":
                continue
            
            #Put tocountry onto list
            tocountries[col][cto] = 1
            
            #Add data into dictionary
            if yeardatacol[col].get(cyear) == None:
                yeardatacol[col][cyear] = {}
            if yeardatacol[col][cyear].get(cfrom) == None:
                yeardatacol[col][cyear][cfrom] = {}
            yeardatacol[col][cyear][cfrom][cto] = ccol[col]
            
    #Output the dictionary data to excel files: one worksheet per year
    for col in range(0,4):
        print("Column "+str(col))
        #Create excel workbook
        wbk = xlwt.Workbook()
        
        #Add each year's data in as a separate worksheet
        for cyear in sorted(yeardatacol[col].keys()):
            print("Year "+cyear)
            sumsheet = wbk.add_sheet(cyear, cell_overwrite_ok=True)
            sumsheet.write(0, 0, tablelabels[col])
            
            #Write list of "to" countries as the header
            i = 1
            for cto in sorted(tocountries[col]):
                sumsheet.write(0, i, cto)
                tocountries[cto] = i
                i = i+1
            
            #Write one row per 'from' country
            row = 1
            for cfrom in sorted(yeardatacol[col][cyear].keys()):
                sumsheet.write(row, 0, cfrom)                
                for cto in sorted(yeardatacol[col][cyear][cfrom].keys()):
                    sumsheet.write(row, tocountries[cto], yeardatacol[col][cyear][cfrom][cto])
                row = row + 1
        
        #Save spreadsheet to file
        wbk.save("refugeecol"+str(col+3)+".xls")    
        
