#!/usr/bin/env python
#This program gets a list of all internet-accessible datastores in data.un.org
#
#These are ordered by mart (datamart = an organisation that gave
#  data to the UN statistics department)
#Datastores are in two forms: as raw files (all the 2-digit stores are like this)
#Or as a choice of xml, csv, pipe-separated and semicolon-separated files.
#
#It also contains code to download all the datasets from data.un.org
#This code is still flaky, i.e. may crash and need to be run multiple times before
#it gets all the files needed.
#
# Example use:
#
#from importUndata import *
#d = ImportUndata()
#d.scrape_all_data()
#
# Sometimes this will fail with errors like "permission denied: 'temp.zip'
# - the fix for this is to call
#d.download_datasets_from_file(datadir, datasetsfile, fromdataset)
#where fromdataset is the name of the dataset that the program was reading when it crashed.
#e.g.
#datadir = "undata_2012-Jul-28-12-00-34"
#indexfile = datadir + "/" + "un_datasets_2012-Jul-28-12-00-35.csv"
#d.download_datasets_from_file(datadir+"/raw", indexfile, "EDATA/cmID%3aBS%3btrID%3a123")
#
#Sara-Jayne Farmer
#2012

from BeautifulSoup import BeautifulSoup
import csv
import glob
import os
import re
import sys
import time
import urllib
import urllib2
import zipfile


#Class to read the datamart titles and ids from a UN dataset page
#by scraping that mart's index webpage.
#Run this with:
#import undatascraper
#d = importUndata.ImportUndata(['EDATA','ENV'])
#datasets = d.readmarts("file.txt")
#Sara-Jayne Farmer
#2012
class ImportUndata:
    Name = "ImportUndata"
    pagetext = ""
    braces = []
    marts = []
    datasets = []
    alldatasets = []

    #Initialise class - nothing needs to be done here
    def __init__(self):
        print("created dataset scraper")


    #Get list of datamarts on the UN open data site (datamart = an organisation that 
    #gave data to the UN statistics department) and write this to a local excel file
    def get_marts_from_webpage(self):

        martspage = "http://data.un.org/Handlers/ExplorerHandler.ashx?t=marts"
        page = urllib2.urlopen(martspage)
        soup = BeautifulSoup(page)

        #FIXIT: Add: Take a local copy of the original file

        #Deconstruct each line of the webpage, and pull out and store the datamart ids
        self.marts = []
        i=1
        while i < len(soup):

            inline = soup.contents[i];

            #First two lines are <Span> tags, with a blank line after each one
            mart = soup.contents[i].contents[0]
            #print(str(i) + "Mart: " + mart.encode('utf-8'))
            source = soup.contents[i+2].contents[0]
            #print(str(i+2) + "Source: " + source.encode('utf-8'))

            #Next is an <img> tag, or an img tag then a space and an <a href> tag
            if (soup.contents[i+4].contents != []):
                imgfile = soup.contents[i].contents[0]
            else:
                imgfile = ""
            #print(str(i+4) + "Image: " + imgfile)

            #move past any remaining tags to the array at the end of the block
            #Once split using splitlines, it contains:
            #ss[1] = title, [2] = childNodes, [3] = isLeaf, [4] = noWrap, [5] = martId,
            #[6] = dataFilter
            #We only use martId for now...
            i = i+5
            if soup.contents[i] == " ":
               i = i+2
            soupstr = (soup.contents[i]).splitlines()
            idstring = soupstr[5]
            martId = idstring[15:len(idstring)-2]
            #print(str(i) + "Mart id: " + martId)
            i = i+1

            #Write this block out as a line in the csv file
            self.marts += [[mart, source, martId]]

        #There doesn't appear to be a close() associated with csvwrite. Okay.
        return(self.marts)


    #Get list of datamarts - from csv file for now, but this will eventually be a function called
    # with a list generated from scraping the datamarts webpage.
    def get_martids_from_file(self, martfile):
        
        martIds = []
        csvin = csv.reader(open(martfile))
        for row in csvin:
            martIds = martIds + [row[2]]
        martIds = martIds[1:len(martIds)] #remove list header
        
        return(martIds)


    #This function is used by readmarts()
    #It finds the end bracket that matches a given start bracket in a list of brackets.
    #Once it has a start and end bracket (some of these are nested), it gets the dataset title
    #martid and datasetid from the characters inside them.
    def findend(self, startindex):

        #Don't do anything if we're run off the end of the list
        #print("Calling findend for brace " + self.pagetext[self.braces[startindex]] +
        #      " index " + str(startindex) + " at position " + str(self.braces[startindex]))
        if (startindex+1 < len(self.braces)):

            #Process all the children of this datastore
            index = startindex+1
            while (self.pagetext[self.braces[index]] == "{"):
                index = self.findend(index)
            
            #Found matching bracket: find the data, write it to datastores file
            #print("processing from " + self.pagetext[self.braces[startindex]] + " " + str(startindex) +
            #      " to " + self.pagetext[self.braces[index]] + " " + str(index))
            
            #Get the title of the current dataset listing - it's between startindex and startindex+1
            #and betweeen the next ">" and "<"
            top = self.pagetext[self.braces[startindex]:self.braces[startindex+1]]
            firstgt = top.find(">")
            top = top[firstgt+1:]
            nextlt = top.find("<")
            storetitle = top[:nextlt]
            
            #The datafilter and martid are between index-1 and index.
            #Look "martId". Anything between the next two ""s is the martId.
            #Later - look for "dataFilter". Anything between the next two ""s is the datasetId.
            bot = self.pagetext[self.braces[index-1]:self.braces[index]]
            filtpos = bot.find("\"dataFilter\"")
            bot = bot[filtpos+13:]
            idstart = bot.find("\"") #We have to do this to allow for extra spaces between ""
            bot = bot[idstart+1:]
            idend = bot.find("\"")
            storeid = bot[:idend]

            bot = self.pagetext[self.braces[index-1]:self.braces[index]]
            martpos = bot.find("\"martId\"")
            bot = bot[martpos+8:]
            idstart = bot.find("\"") #We have to do this to allow for extra spaces between ""
            bot = bot[idstart+1:]
            idend = bot.find("\"")
            martid = bot[:idend]

            print("New dataset " + martid + "/" + storeid + ", title: " + storetitle)
            self.datasets = self.datasets + [[martid, storeid, storetitle]]
            
        return index+1


    #This function reads in the page text as an array of text, then finds the dataset titles
    #and ids in it. It's crude, but it gets around the read errors seen when using BeautifulSoup
    #NB Every dataset is between the markers "{" and "}" in the array. Some datasets are nested.
    def get_datasets_list_from_webpage(self, martId):

        #Read in dataset page
        page = urllib2.urlopen("http://data.un.org/Handlers/ExplorerHandler.ashx?m="+martId)
        self.pagetext = page.read(page)

        #Create list of brackets ({}) on page
        self.braces = [m.start() for m in re.finditer("{|}", self.pagetext)]
        self.braces = self.braces[1:len(self.braces)-1] #remove outer braces
        #print("Found " + str(len(self.braces)) + " braces")

        #Get dataset titles and ids from the page, using the bracket list
        self.datasets = []
        index = 0
        while (index < len(self.braces)):
            index = self.findend(index)
        
        return self.datasets
    
    
    #Download all csv datafiles from data.un.org
    def download_datasets_from_file(self, datadir, datasetsfile, fromdataset):
        
        #Set marker for downloading partial datasets (needed to get round bug)
        if fromdataset == "":
            fromfound = True
        else:
            fromfound = False
        
        #Point at UNdata's download URLs
        urlRoot      = "http://data.un.org/Handlers/DownloadHandler.ashx?DataMartId="
        digiturlRoot = "http://data.un.org/Handlers/DocumentDownloadHandler.ashx?t=bin&id="

        #Go through list of datasets, and pull in the file for each one
        csvReader = csv.reader(open(datasetsfile, 'rb'))
        csvReader.next() #Ignore header line
        for row in csvReader:
            
            martId = row[0]
            datasetId = row[1]
            title = row[2]

            #Check for start of download, if needed
            if fromfound == False:
                if fromdataset == martId + "/" + datasetId:
                    fromfound = True
                else:
                    continue

            #FIXIT: null value put into this file is horrible. Change it!
            #stop trying to process header line
            if datasetId.find("null\r\n") == -1:

                #KI (Global Indicator Database) is different to the other datasets - it gives a
                #pointer to other martIds and datasetIds, embedded in its datasetId entry as
                #"dataSetID%3a<martId>%3b<datasetId>"
                if (martId == "KI"):
                    print("Key performance indicator found")
                    mstart = datasetId.find("%3a")
                    dstart = datasetId.find("%3b")
                    martId = datasetId[mstart+3:dstart]
                    datasetId = datasetId[dstart+3:]
                
                print(martId+ '/'+ datasetId+ ': '+ title)

                timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())
                outfileRoot = datadir + "/" + martId + "_" + datasetId + "_" + timestamp
                
                if (martId.isdigit()):
                    #Handle case where there's only one data format available
                    print('Only one data format available: storing excel')
                    docId = datasetId[6:]
                    page = urllib2.urlopen(digiturlRoot+docId)
                    #Need to use docId because the semicolon truncates the filename
                    f = open(datadir + "/" + martId + "_" + docId + "_" + timestamp + ".xls", "wb")
                    data = page.read()
                    f.write(data)
                    f.close()
                    
                else:
                    #Handle case where there are 4 formats available
                    print('Multiple data formats available: storing csv')
                    docRoot = urlRoot + martId + "&DataFilter=" + datasetId + "&Format="

                    #for datatype in ['csv', 'xml']:
                    for datatype in ['csv']: #only pull the csv for now - it's smaller
                        name = "temp.zip"
                        name, hdrs = urllib.urlretrieve(docRoot + datatype, name)
                        z = zipfile.ZipFile(name)
                        for n in z.namelist():
                            f = open(outfileRoot + "." + datatype, 'wb')
                            data = z.read(n)
                            f.write(data)
                            f.close()
                            
                        z.close()
                        os.unlink(name)


    #Concatenate the data in a directory full of csv
    def concatenate_marts(self):
        
        csvout = csv.writer(open('un_mart_all.csv', 'wb'), quoting=csv.QUOTE_NONNUMERIC)
        csvout.writerow(['martId', 'datasetLabel', 'datasetId'])

        path = 'un_mart_good_data/'
        for infile in glob.glob(os.path.join(path, '*.csv')):
            print("Adding file: "+infile)

            csvin = csv.reader(open(infile))
            for row in csvin:
                csvout.writerow(row)

        print("Finished. Results are in un_mart_all.csv")


    #Main function: download list of marts, list of datasets, and datasets themselves
    def scrape_all_data(self):

        #Create directory for indices and data
        timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())
        datadir = "undata_" + timestamp
        os.mkdir(datadir)
        
        #Get list of datamarts on data.un.org
        marts = self.get_marts_from_webpage()

        #Write list of datamarts to a file
        timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())
        martfile = datadir + '/un_marts_' + timestamp + '.csv'
        f = open(martfile, 'wb')
        csvout = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        csvout.writerow(['mart', 'source', 'martId'])
        for mart in self.marts:
            csvout.writerow(mart)
        f.close()

        #Get list of datastores on data.un.org: write to a file
        timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())
        datasetsfile = datadir + '/un_datasets_' + timestamp + '.csv'
        f = open(datasetsfile, 'wb')
        csvout = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        csvout.writerow(['martId', 'datasetId', 'dataset title'])
        self.alldatasets = []
        for m in self.marts:
            martdatasets = self.get_datasets_list_from_webpage(m[2])
            for dataset in martdatasets:
                csvout.writerow(dataset)
                self.alldatasets += [dataset]
        f.close()

        #Download all the excel and CSV datastores from data.un.org
        rawdir = datadir + "/rawdata"
        os.mkdir(rawdir)
        self.download_datasets_from_file(rawdir, datasetsfile, "")
        
        return()


