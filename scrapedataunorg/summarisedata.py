#!/usr/bin/env python
# -*- coding: cp1252 -*-

#This program creates summaries of the headings and indices in a dataset
#
#Example use:
#
#from summarisedata import *
#infodir = "../data/dataunorg_2012-Jul-28-12-00-34"
#datadir = infodir + "/rawdata"
#indexfile = infodir + "/undatacsvfiles_2012-Jul-29-13-34-37.csv"
#masterfile = "../data/master lists/dataunorg_datasets.csv"
#[titles, indices] = summarise_directory(infodir, datadir, True)
#nonalphas = find_nonalphanumeric(masterfile, 3)
#create_buzzfilenames(masterfile)
#update_dataunorg_master(masterfile, indexfile)
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

#======================================================================================
#Find data.un.org index files in a given directory, and read information in from them
#Assumes that there are 2 files to find:
# un_datasets*   : list of data.un.org datasets
# un_marts*      : list of data.un.org datamarts
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def read_index_files(indexdir):
    
    #Reset dictionaries
    martowners = {}
    marttitles = {}
    datasettitles = {}

    fstr = '(.+?)%3a(.+?)%3b(.+?)$' #Search string for unpacking KI datasetIds
    indexfiles = glob.glob(os.path.join(indexdir, '*.csv'))
    for infile in indexfiles:
        filename= infile[len(indexdir)+1:]
        if filename.startswith("un_datasets"):
            print("Using dataset index "+filename)
            f = open(infile, 'rb')
            csvReader = csv.reader(f)
            headers = csvReader.next()
            for row in csvReader:
                martId       = row[0]
                datasetId    = row[1]
                datasetTitle = row[2]
                
                #Ignore empty datasets (these are the headers for groups)
                if datasetId.strip() == "null":
                    continue
                
                #Handle dataset (KI) that references the other marts
                #and *not* with the same fileset
                if martId == "KI":
                    #print("KI. datasetId is:"+datasetId+":")
                    ids = re.findall(fstr, datasetId)
                    martId    = ids[0][1]
                    datasetId = ids[0][2]
                    
                datasettitles[martId+"_"+datasetId] = datasetTitle
            f.close()
            
        elif filename.startswith("un_marts"):
            print("Using datamart index "+filename)
            f = open(infile, 'rb')
            csvReader = csv.reader(f)
            headers = csvReader.next()
            for row in csvReader:
                martTitle = row[0]
                martOwner = row[1]
                martId    = row[2]
                marttitles[martId] = martTitle
                martowners[martId] = martOwner
            f.close()
    
    return([martowners, marttitles, datasettitles])


#======================================================================================
#Create simple histograms of headers and indices in all csv files in a
#given directory, where "footnote" in the index field denotes the end of
#the data area.
#
#Index directory is expected to contain 2 files:
# * un_datasets_<date>.csv
# * un_marts_<date>.csv
#
#Datadir is the directory containing the datafiles
#
#Outputs 3 files:
# undatafiles_<timestamp>.csv: summary statistics for each datafile
# undataheadings_<timestamp>.csv: summary statistics for each top-row entry
# undataindices_<timestamp>.csv: summary statistics for each left-column entry
# 
#Sara-Jayne Farmer
#2012
#======================================================================================
def summarise_directory(indexdir, datadir, writefiles):

    #Create counter and array objects
    titles = collections.Counter()
    indices = collections.Counter()

    #Grab the index information from the index directory
    print("Creating summaries of directory "+datadir)
    [martowners, marttitles, datasettitles] = read_index_files(indexdir)
    
    #Create csv file to contain file summaries
    if writefiles == True:
        timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())
        fout = open("undatacsvfiles_"+timestamp+".csv", "wb")
        c = csv.writer(fout)
        c.writerow(["Mart Id","Dataset Id","Download Date","Number of Rows","Dataset Title","Headers (next few columns)"])

    #Pull in all the csv files from the data directory
    fstr = '(.+?)_(.+?)_(.+?)\.(.+?)$' #Search string for infile contents
    csvfiles = glob.glob(os.path.join(datadir, '*.csv'))
    for infile in csvfiles:

        #Grab martId, datasetId and download date from the filename.
        filename= infile[len(datadir)+1:]
        print("==Adding file: " + filename)        
        ids = re.findall(fstr, filename)
        martId    = ids[0][0]
        lenids = len(ids[0]) #There are more than two underscores in some datasetnames. Deal with it.
        dotpos = filename.rfind(".")
        scorepos = filename.rfind("_")
        if len(ids[0][2]) == (dotpos-scorepos-1):
            datasetId = ids[0][1]
            filedate  = ids[0][2]
        else:
            datasetId = filename[len(martId)+1:scorepos]
            filedate = filename[scorepos+1:dotpos]

        #Read in file
        fin = open(infile, 'rb')
        csvReader = csv.reader(fin)

        #Grab the header row, and store to list
        headers = csvReader.next()
        for header in headers:
            titles[header] += 1
            #if header.find('Area'): print("Area in "+filename)
        
        #Grab all the non-footnote, non-empty indices
        numrows = 0
        for row in csvReader:
            numrows = numrows+1
            if len(row) > 0:
                index = row[0]
                if index.startswith("footnote") or index.startswith("Footnote") \
                   or index.startswith("fnSeqID"):
                    break

                #Log this index
                #NB strip() removes leading and trailing whitespace
                indices[index.strip()] += 1
                if infile.startswith("IFS"): #Include countrynames from IFS files
                    indices[row[1].strip()] += 1

        #Store file details in the file summary csv
        if writefiles == True:
            martTitle = marttitles[martId]
            datasetTitle = datasettitles[martId+"_"+datasetId]
            c.writerow([martId, datasetId, filedate, str(numrows), datasetTitle] + headers)

        fin.close()

    #Close file summary csv
    fout.close()

    #Dump the header and index summaries out to files.
    if writefiles == True:
        f = open("undatacsvheadings_"+timestamp+".csv", "wb")
        c = csv.writer(f)
        c.writerow(["Heading","Count"])
        for i in sorted(titles.keys()):
            c.writerow([i,str(titles[i])])
        f.close()

        f = open("undatacsvindices_"+timestamp+".csv", "wb")
        c = csv.writer(f)
        c.writerow(["Index","Count"])
        for i in sorted(indices.keys()):
            c.writerow([i, str(indices[i])])
        f.close()

    return([titles, indices])


#======================================================================================
#Find all characters that might be an issue in a given csv and column
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def find_nonalphanumeric(csvfile, column):

    #Use a set object to hold all the unique nonalpha characters
    allnonalphas = set()
    
    fin = open(csvfile, 'rb')
    csvReader = csv.reader(fin)

    #Ignore the header row
    headers = csvReader.next()
    for row in csvReader:
        if len(row) >= column+1:
            #print("looking in " + row[column])
            strnonalphas = re.findall("\W", row[column])
            allnonalphas |= set(strnonalphas)

    fin.close()
    
    return(allnonalphas)


#======================================================================================
#Find all characters that might be an issue in a given csv and column
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def strip_datasettitle(filename, martid):
    
    buzzfile = filename
    if martid == "ComTrade":
        buzzfile = buzzfile[31:] #Strip off "Trade of goods , US$, HS 1992, "

    #Convert $ to dollar and % to percent and & to and and > to gt
    dic = {'$':' dollar ', '%':' percent ', '&':' and ', '>':' gt '}
    for i, j in dic.iteritems():
        buzzfile = buzzfile.replace(i, j)
    #Convert remaining non-alphanumerics to spaces
    buzzfile = re.sub('[\W]', ' ', buzzfile)
    #Remove double spaces
    buzzfile = re.sub('( +)', ' ', buzzfile)
    #Strip leading and trailing spaces
    buzzfile = buzzfile.strip()

    return(buzzfile)


#======================================================================================
#Find all characters that might be an issue in a given csv and column
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def create_buzzfilenames(csvfile):

    fin = open(csvfile, 'rb')
    csvReader = csv.reader(fin)
    fout = open("datawithbuzznames.csv", "wb")
    c = csv.writer(fout)

    #Header row
    headers = csvReader.next()
    c.writerow(headers + ["Buzz filename"])

    #Name rows    
    for row in csvReader:
        if len(row) < 4:
            buzzfile = ""
        else:        
            buzzfile = strip_datasettitle(row[2], row[0])
            
        #Add new line to output file
        c.writerow(row + [buzzfile])

    fin.close()
    fout.close()

    return()



#======================================================================================
#Update master index for data.un.org with info from new data.un.org download
#
# After this is done, any row with a last upload date of "" will need adding into
# the Buzzdata website.
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def update_dataunorg_master(masterfile, indexfile):
    
    #Read master file into dictionaries
    filesegments  = {}
    datasettitles = {}
    buzzdatarooms = {}
    buzzfilenames = {}
    lastdownloads = {}
    lastuploads   = {}
    numrows       = {}
    headers       = {}
    
    fmaster = open(masterfile, 'rb')
    csvmaster = csv.reader(fmaster)
    masterheaders = csvmaster.next()
    
    for row in csvmaster:
        fileid = row[0] + "/" + row[1]
        #print(fileid + str(len(row)))
        filesegments[fileid]  = row[2]
        datasettitles[fileid] = row[3]
        buzzdatarooms[fileid] = row[4]
        buzzfilenames[fileid] = row[5]
        lastdownloads[fileid] = row[6]
        lastuploads[fileid]   = row[7]
        numrows[fileid]       = row[8]
        headers[fileid]       = row[9:]
    fmaster.close()
    
    #Open output master file
    fout = open("newmaster.csv", "wb")
    c = csv.writer(fout)
    c.writerow(masterheaders)

    #Read index file, adding new files to master, and checking details against last upload
    findex  = open(indexfile, 'rb')
    csvindex  = csv.reader(findex)
    headers = csvindex.next()
    for row in csvindex:
        fileid = row[0] + "/" + row[1]
        martid          = row[0]
        datasetid       = row[1]
        downloaddate    = row[2]
        downloadrows    = row[3]
        downloadtitle   = row[4]
        downloadheaders = row[5:]

        if numrows.has_key(fileid):
            filesegment = filesegments[fileid]
            dataroom    = buzzdatarooms[fileid]
            buzzfile    = buzzfilenames[fileid]
            
            #Reset upload date to force new upload if the data has changed
            if downloadrows == numrows[fileid] and downloadheaders == headers[fileid]:
                lastupload = lastuploads[fileid]
            else:
                lastupload = ""
        else:
            #Haven't seen this dataset before: add it to the master file
            filesegment = "all"
            dataroom    = ""
            buzzfile    = strip_datasettitle(downloadtitle, martid)
            lastupload  = ""

        c.writerow([martid, datasetid, filesegment, downloadtitle, dataroom, buzzfile,
                    downloaddate, lastupload, downloadrows] + downloadheaders)

    findex.close()
    fout.close()

    return()

