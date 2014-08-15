#!/usr/bin/env python
# -*- coding: cp1252 -*-
#
#This program cleans the excel files found in data.un.org into sets of
#CSV files (which are much easier to handle)
#
#Example use:
#
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
class CleanExcel:
    Name = "CleanExcel"
    
    #Clean excel files in data.un.org
    #
    #Sara-Jayne Farmer
    #2012
    def convertDataUNorg(self, mart, datafile):
        
        #Open file
        book = xlrd.open_workbook(datafile)
        
        if mart == "15":
            print("Mart 15")
            #Mart 15:
            #- One worksheet
            #- Notes in rows 1:2,
            #- Header titles split over rows 4:5,
            #- at least one header title (273, 275) split over rows 4,5,6,7
            #- Some header titles merged across columns
            #- Some files have blank "spacer" columns
            #- lhs index is countries in column B
            #- Implicit headers (e.g. "Very High Human Development"
            #  embedded in the lhs index (as cell merged across columns)
            #- Summary table ("HDI groupings" or no header) at end of data
            #- contains both human development level and regions
            #- (no summary table in 275)
            #- endnotes starting with "NOTES" or "NOTE" in column A
            #- missing data marked as ".."

            DevStatuses = [
                "Very high human development",
                "High human development",
                "Medium human development",
                "Low human development"]

        elif mart == "16":
            print("Mart 16")
            #Mart 16:
            #- 4 worksheets: 1 data, 1 footnotes, 1 source, 1 tech notes
            #(Split into data and notes)
            #- Notes in rows 1:2
            #- Header titles in row 3:4 or 3:6
            #- Header titles split over columns,
            #- Some columns (notes) have no header
            #- Blank "spacer" columns
            #- LHS index is countries in column A; just countries
            #- missing data marked as "..."
            #- 286 uses "<" in amongst number fields
            
        elif mart == "18":
            print("Mart 18")
            #Mart 18:
            #- 4 worksheets, each with different data
            #  (make big table from these, or split into files?)
            #- Notes (worksheet title) in row 3 or 4
            #- Header titles in row 5 or 6
            #- LHS index is countries in column A; just countries
            #- missing data marked as ".."

        elif mart == "19":
            print("Mart 19")
            #Mart 19:
            #- 2 worksheets, second one blank
            #- Notes in rows 1:4 (inc date)
            #- 3d table represented in 2d.
            #  (Split into files by label)
            #- Header in row 6
            #- Column c has no header but contains notes
            #- Column c note ids (1,2 etc) are restarted per country
            #- LHS index is country codes (just codes+names) in col A/B
            #- Col A only has one entry per country; col B is filled in.
            #- missing data marked as ".."
            #- Footnotes, with no footnote marker, in column D at end of table
            #  (Check for empty columns a:c?)
            #- Footnote after those.      
            
        elif mart == "22":
            print("Mart 22")
            #Mart 22:
            #- 6 worksheets, 3 data, 3 notes
            #  (split into files by page)
            #- 3d table represented in 2d
            #  (split into files by label)
            #- Notes in row 1:2
            #- Header in row 3:4 or 3:5
            #- LHS index is countries (just countries) in col A
            #- missing data marked as ".."

        elif mart == "25":
            print("Mart 25")
            #Mart 25:
            #- 7 worksheets, 4 data, 3 notes
            #- (split into files by page)
            #- 3d table (country, year, label) represented in 2d
            #  (split into files by label)
            #- Notes in row 1:2
            #- Header in row 3 or 3:4
            #- LHS index is countries (just countries) in col A
            #- missing data marked as "0.0"

        elif mart == "29":
            print("Mart 29")
            #Mart 29:
            #- 4 or 9 worksheets, 1 or 6 data, 3 notes
            #- (split into files by page)
            #- 3d table (country, year, label) represented in 2d
            #  (split into files by label)
            #- Notes in row 1:16 or 1:14
            #- Header in row 17:19 or 15:16
            #- LHS index is countries (just countries) in col A
            #- missing data marked as ".."

        elif mart == "30":
            print("Mart 30")
            #Mart 30:
            #- 2 worksheets (1 data, 1 notes)
            #- 3d table (country, year, label) represented in 2d
            #  (split into files by label)
            #- Header in row 1
            #- LHS index is countries (just countries) in col B
            #- missing data marked as ""
            #- Footnotes at end of data sheet, after blank lines
            #  (marker text is "Footnote:" in col B)

        elif mart == "31":
            print("Mart 31")
            #Mart 31:
            #- single worksheet
            #- 2d table (country, label)
            #- Notes in row 1
            #- Header in row 2-4
            #- Notes columns have no headers
            #- LHS index is countries (just countries) in col A-B
            #- missing data marked as "..."
            #- Footnotes at end of data sheet
            #  (marker text is "Note:" in col A-B)                    

        else:
            print("God knows what this is")
            #Other excel files - convert to csv

        return()
