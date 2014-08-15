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
#IMPORTANT: you will need these files in the same directory, or the code won't run:
#  (codes/UNSTATSErrorDictionary.csv, codes/UNSTATSplacecode.csv) or 
#  (codes/ISO3166ErrorDictionary.csv)
#
#Example use:
#
#from cleanIndices import *
#c = CleanIndices()
#rawdir = '../data/dataunorg_2012-Jul-28-12-00-34/rawdata'
#c.check_indices_in_csv("indices_names.csv", "UNSTATS")
#c.check_indices_in_csv("indices_names.csv", "ISO3166")
#c.find_in_indices(rawdir, "Sudan")
#c.gisclean_directory(rawdir, ["UNSTATS","ISO3166"], "n", "n")
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
import time
import xlrd
from Tkinter import *


#======================================================================================
#Clean up data in arrays where the first column in each array is an index
# - usually country, sometimes region or economic status
#And we expect the files to also contain footnotes
#
#Sara-Jayne Farmer
#2012
#======================================================================================
class CleanIndices(Frame):
    
    Name = "CleanIndices"
    indexcodes   = [] #Index standards currently being applied
    validindices = {} #Indices in current standard
    validlower   = {} #Lowercase version of valid indices
    indexerrors  = {} #Error list for current standard
    withdrawn    = {} #Withdrawn list for current standard
    withlower    = {} #Lowercase version of withdrawn list
    subserrors   = {} #Common substring errors, e.g. abbreviations


    #======================================================================================
    #Create GUI for this tool
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        return(None)


    #======================================================================================
    #Put buttons etc on the GUI
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def createWidgets(self):
        self.quitButton = Button (self, text='Quit', command=self.quit)
        #self.doButton = Button(self, text="Do Something", command=self.doSomething)

        self.quitButton.grid()
        #self.doButton.grid()
        return()


    #======================================================================================
    #Draw coloured world map of index counts
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def map_counts(self, countcsv):

        #Read counts in from csv file
        counts = {}
        f = open(countcsv, 'rb')
        csvReader = csv.reader(f)
        headers = csvReader.next()
        for row in csvReader:
            counts[row[0]] = row[1]
        f.close()
        
        #Sort countries by count size
        for i in sorted(counts.keys()):
            sortedcounts[i] = counts[i]

        #Divide space into n blocks and allocate colours to those blocks
        #NB we expect a plot of sorted counts will be logarithmic

        #Read in map template

        #Colour in map

        #Save map

        return()        


    #======================================================================================
    #Load in list of countries and regions from the 'official' standards;
    #Currently either the UN list from data.un.org or ISO3166
    #NB some UN indices have no codes associated with them
    #FIXIT: add code to bomb out if the input file doesn't exist
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def create_valid_lists(self, codeused):

        #Only create codes if they're not already on the list
        if not self.validindices.has_key(codeused):
            self.validindices[codeused] = {}
            self.validlower[codeused]   = {}

            if codeused == "ISO3166":
                #ISO3166 is being used: get the valid names from pycountry
                for i in range(0,len(pycountry.countries)):
                    idict = list(pycountry.countries)[i]
                    ccode = idict.alpha3
                    cname = idict.name
                    self.validlower[codeused][string.lower(cname)] = cname
                    self.validindices[codeused][cname] = ccode

            else:
                #UNSTATS is being used: get the valid names from a file
                f = open('codes/UNSTATSPlaceCodes.csv', 'rb')
                csvReader = csv.reader(f)

                #Skip header row, then load in all the countries etc.
                #Make index lowercase, to make searching easier
                headers = csvReader.next()
                for row in csvReader:
                    ccode = row[1]
                    cname = row[2]
                    self.validlower[codeused][string.lower(cname)] = cname
                    self.validindices[codeused][cname] = ccode
                f.close()
            
        return()
    

    #======================================================================================
    #Load in list of known errors
    #This maps all the countrynames that can't be corrected
    #to the corresponding name fields in ISO-3166:
    #see https://bitbucket.org/techtonik/pycountry/src/09533299c041/src/pycountry/databases/iso3166.xml
    #Notes:
    # Cote d'Ivoire has an accent
    # there are 2 Ethiopias in ISO3166 with name "Ethiopia", depending on date
    # there are 3 Germanies (germany dem rep, germany fed rep)
    # there are two Koreas (Korea dem rep, Korea rep)
    # there are two Congos (Congo dem rep and Congo rep)
    # there are 2 Pacific Islands (Pacific islands trust, Pacific islands USA)
    # Venezuela has a lowercase "r" in the ISO3166 standard name
    # there are 3 Yemens (Yemen former rep, Yeme former dem rep, Yemen rep)
    #
    #Also create list of countries withdrawn from ISO3166 or the UNstats list on data.un.org
    #Notes:
    # Netherlands Antilles has also been withdrawn
    #
    #Sara-Jayne Farmer
    #
    #2012
    #======================================================================================
    def create_error_lists(self, codeused):
        
        #Only create codes if they're not already on the list
        if not self.indexerrors.has_key(codeused):
            self.subserrors  = {}
            self.indexerrors[codeused] = {}
            self.withdrawn[codeused]   = {}
            self.withlower[codeused]   = {}

            #Create list of substring errors, e.g. common abbreviations
            self.subserrors["^mdg_"] = ""  #Remove "mdg_" from start of country names
            self.subserrors["  "]    = " "   #Double spaces happen too
            self.subserrors["dem\."] = "democratic"
            self.subserrors["rep\."] = "republic"
            self.subserrors["fed\."] = "federated" #FIXIT: Also covers federal, which is a bit of a problem
            self.subserrors["isds"]  = "islands"
            self.subserrors["is\."]  = "island"
            self.subserrors[" is$"]  = " island" #"is" at end of line only, eg "Wallis is" -> "Wallis island"
            self.subserrors["^st "]  = "saint " #"st " at start of line only, e.g. "st blast and x" -> "saint blast and x"
            self.subserrors["st\."]  = "saint"
            self.subserrors[" & "]   = " and "      
            self.subserrors["\["]    = "("   
            self.subserrors["\]"]    = ")"   

            
            #Get error dictionary for the standard being applied
            #File has header row; data rows have form [data.un.org name, issue, correct name/code]
            if codeused == "ISO3166":
                infile = "codes/ISO3166ErrorDictionary.csv"

                #Also add all the official_names in pycountries into the error list
                #Using the official name instead of name is a common mistake
                for i in range(0,len(pycountry.countries)):
                    try:
                        idict = list(pycountry.countries)[i]
                        offname = idict.official_name
                        self.indexerrors[codeused][string.lower(offname)] = string.lower(idict.name)
                    except:
                        continue
            
            else:
                infile = "codes/UNSTATSErrorDictionary.csv"

            f = open(infile, 'rb')
            csvReader = csv.reader(f)

            #Ignore header row and read in all the data rows
            headers = csvReader.next()
            for row in csvReader:
                if len(row) == 0:
                    break
                if row[1] == "withdrawn":
                    self.withlower[codeused][string.lower(row[0])] = row[0]
                    self.withdrawn[codeused][row[0]] = row[2]
                else:
                    self.indexerrors[codeused][string.lower(row[0])] = string.lower(row[2])

            f.close()
        
        return()
  

    #======================================================================================
    #Clean up an input country code:
    #Change the index to one that meets a given standard (ISO-3166 or UNSTATS)
    # and return 3-digit code for the index
    # or "---" if it's not a valid index
    #
    #Sara-Jayne Farmer
    #
    #2012
    #======================================================================================
    def check_index(self, indexin, codeused):

        #Load lists of valid indices and known errors for the input standard
        #----------------------------------------------
        if codeused not in self.indexcodes:
            self.create_valid_lists(codeused) #Current codes
            self.create_error_lists(codeused) #Known errors
            self.indexcodes += [codeused]

        
        #Remove common errors (trailing whitespace etc)
        #----------------------------------------------

        #convert input index into lowercase - this makes search easier, and stops  
        #us having to duplicate substitions with lower and uppercase versions
        indexout = string.lower(indexin)

        #Substring spelling errors
        indexout = indexout.strip()           #Trailing and leading whitespace
        indexout = indexout.replace(" +", "") #Trailing "+" - might need to specify "at end"
        for subs in self.subserrors.keys():   #Common abbreviations
            indexout = re.sub(subs, self.subserrors[subs], indexout)

        #UNICEF using brackets instead of commas
        if codeused == "ISO3166" and re.findall("\(", indexout):
            indexout = re.sub(" \(", ", ", indexout)
            indexout = re.sub("\(", ", ", indexout) #catch any brackets without spaces before
            indexout = re.sub("\)", '', indexout)

        #If index is on common errors list, swap it for corrected index
        if self.indexerrors[codeused].has_key(indexout):
            indexout = self.indexerrors[codeused][indexout]

        #print("1. indexout ["+indexout+"]")

        #Look for index in lists of valid and withdrawn indices
        #-----------------------------------------
        indexcleaned = "y"

        #Start by looking for index in the list of lowercase valid indices
        if self.validlower[codeused].get(indexout) != None:
            indexout = self.validlower[codeused][indexout]
            indexcode = self.validindices[codeused][indexout]
            
        #Then try the list of deprecated countries
        elif self.withlower[codeused].get(indexout) != None:
            indexout = self.withlower[codeused][indexout]
            indexcode = self.withdrawn[codeused][indexout]
            
        #Accept that we really can't find this name in the list
        else:
            #print("Missing code for [" + indexin + "], tried [" + indexout + "]")
            indexcode = "---"
            indexout = ""
            indexcleaned = "x"

        if indexout == indexin:
            indexcleaned = "n"

        return [indexcleaned, indexout, indexcode]



    #======================================================================================
    #Check list of indices in csv file with a header and row format index, count 
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def check_indices_in_csv(self, csvfile, codeused):

        fin = open(csvfile, 'rb')
        fout = open("tmp_indexerrors.csv", 'wb')
        fcnt = open("tmp_placecount.csv", 'wb')
        csvReader = csv.reader(fin)
        csvWriter = csv.writer(fout)
        csvCount = csv.writer(fcnt)

        counts = collections.Counter()
        correctnames = {}
        correctcodes = {}
        countcode = {}

        #Ignore header and check all the indices in the following rows
        #Output results to file tmp_placecount.csv
        headers = csvReader.next()
        for row in csvReader:
            if len(row) == 0:
                break
            
            index = row[0]
            [indexcleaned, outname, outcode] = self.check_index(index, codeused)
            correctnames[index] = outname
            correctcodes[index] = outcode
            if outcode == "---":
                #print("Missing code for index [" + index + "]")
                continue
            counts[outname] += int(row[1]) #Add count for misspelling to the corrected name
            countcode[outname] = outcode

        fin.close()

        #Write all corrections to a file
        #Do it this way so we only store one of each correction in the file
        csvWriter.writerow(["Input index", "Cleaned index", "Class", "Type", "Corrected"])
        for index in correctnames:
            
            outname = correctnames[index]
            outcode = correctcodes[index]
            if outname == index:
                corrected = "no"
            else:
                corrected = "yes"
            csvWriter.writerow([index, outname, '', outcode, corrected])
        fout.close()

        #Write counts for each valid placename to a file
        csvCount.writerow(["Index", "Code", "Count"])
        for outname in counts:
            csvCount.writerow([outname,countcode[outname],str(counts[outname])])
        fcnt.close()

        return()


    #======================================================================================
    #Clean GIS references in all the csv files in a given directory
    #Cleaned files go to new directory "GIScleaned"
    #
    #Datadir is the directory containing the datafiles
    #Standard is the list of standards that we want names cleaned to. Choices are:
    # "ISO3166", "UNSTATS", "FIPS10", "STANAG"
    #Verbose tags whether we want to see the conversions side-by-side with the originals
    #or not. Verbose="y" adds two columns to each file: code and corrected name, and keeps
    #the original country name column; verbose="n" replaces the original country names with
    #corrected ones.
    #Footnotes tags whether we want to include footnotes in the output or not. "y" means
    #footnotes are copied across verbatim; "n" means footnotes are ignored.
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def gisclean_directory(self, datadir, standards, verbose, footnotes):

        #Create directory for all the clean files
        timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())
        cleandir = "cleaned_" + timestamp
        os.mkdir(cleandir)
                
        #Pull in all the csv files from the data directory
        csvfiles = glob.glob(os.path.join(datadir, '*.csv'))
        for infile in csvfiles:
            
            #print("==Adding file: " + infile)
            filename= infile[len(datadir)+1:]
            print("cleaning " + filename)
            fin = open(infile, 'rb')
            fout = open(cleandir + "/" + filename, "wb")
            csvIn = csv.reader(fin)
            csvOut = csv.writer(fout)

            #Grab the header row, and store in new file, with code columns added to it
            insert = []
            headers = csvIn.next()
            if verbose == "y":
                for standard in standards:
                    insert += [standard+" cleaned", standard+" code",standard+" name"]
            else:
                for standard in standards:
                    insert += [standard]
            
            if infile.startswith("IFS"): #Countrynames are in 2nd column in IFS files
                csvOut.writerow(headers[0]+insert+headers[1:])
            else:
                csvOut.writerow(insert+headers)
            
            #Grab all the non-footnote, non-empty indices
            numrows = 0
            for row in csvIn:

                #Ignore empty rows
                if len(row) == 0:
                    csvOut.writerow([])
                    continue

                #Add footnotes back into the data, if requested
                index = row[0]
                if index.startswith("footnote") or index.startswith("Footnote") \
                   or index.startswith("fnSeqID"):
                    if footnotes == "y":
                        csvOut.writerow(row)
                        for row in csvIn:
                            csvOut.writerow(row)
                    break

                #Special for 2 country column data
                if datadir == "sjffromto":
                    cfrom = row[0]
                    cto = row[1]
                    [indexcleaned, outname, fromcode] = self.check_index(cfrom, standard)
                    [indexcleaned, outname, tocode] = self.check_index(cto, standard)
                    csvOut.writerow([fromcode,tocode] + row[2:])
                    continue

                #Correct index, if possible, otherwise continue with original index value
                if infile.startswith("IFS"): #Countrynames are in 2nd column in IFS files
                    index = row[1]
                insert = []
                for standard in standards:
                    [indexcleaned, outname, outcode] = self.check_index(index, standard)
                    if verbose == "y":
                        insert += [indexcleaned,outcode,outname]
                    else:
                        insert += [outcode]
                insert += [index]
                
                if infile.startswith("IFS"): #Countrynames are in 2nd column in IFS files
                    csvOut.writerow(row[0]+insert+row[2:])
                else:
                    csvOut.writerow(insert+row[1:])

            #Close input and output files
            fin.close()
            fout.close()


    #======================================================================================
    #Find GIS headers in the csv files in a given directory
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def find_gis_headers(self, datadir):
        
        giscodes = ["national station id number"]
        
        #Pull in all the csv files from the data directory
        csvfiles = glob.glob(os.path.join(datadir, '*.csv'))
        for infile in csvfiles:

            filename= infile[len(datadir)+1:]
            f = open(infile, 'rb')
            csvReader = csv.reader(f)

            #Grab the header row, and store to list
            headers = csvReader.next()
            for header in headers:
                if string.lower(header) in giscodes:
                    print(header + " in "+filename)

            
    #======================================================================================
    #Find a given search term in indices in the csv files in a given directory
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def find_in_indices(self, datadir, searchtermin):
        
        giscodes = ["national station id number"]
        
        #Pull in all the csv files from the data directory
        searchterm = string.lower(searchtermin)
        csvfiles = glob.glob(os.path.join(datadir, '*.csv'))
        for infile in csvfiles:

            filename= infile[len(datadir)+1:]
            f = open(infile, 'rb')
            csvReader = csv.reader(f)

            #Look for the searchterm in the indices
            headers = csvReader.next()
            numrows = 0
            for row in csvReader:
                numrows = numrows+1
                if len(row) == 0:
                    continue
                
                index = row[0]
                if index.startswith("footnote") or index.startswith("Footnote") \
                   or index.startswith("fnSeqID"):
                    break

                if infile.startswith("IFS"): #Include countrynames from IFS files
                    index = row[1]
                    
                if string.find(string.lower(index), searchterm) != -1:
                    print(index + " in "+filename + " row " + str(numrows))


#======================================================================================
#Main loop
#
#Sara-Jayne Farmer
#2012
#======================================================================================

##app = CleanIndices()
##app.master.title("GIS Index Cleaner")
##app.mainloop()
