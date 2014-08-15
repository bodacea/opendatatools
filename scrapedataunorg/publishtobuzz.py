#!/usr/bin/env python
# -*- coding: cp1252 -*-

#Connect dataset to buzz data website
#
#Example use:
#from publishtobuzz import *
#apikey = setup("apikey.txt")
#filelist = get_filelist("un-energy-statistics-bagasse", apikey)
#roomlist = get_roomlist(apikey)
#localfile = "development_organisations.csv"
#rr = "this is a release note"
#res = add_file("sara/testroom", "test_buzzfile4", localfile, rr, apikey)
#apifile = "apikey.txt"
#datadir = "../data/dataunorg_2012-Jul-28-12-00-34/cleaned_2012-Jul-29-17-01-56"
#masterindexcsv = "../data/master lists/dataunorg_datasets.csv"
#upload_to_buzz(datadir, masterindexcsv, apifile)
#
#Sara-Jayne Farmer
#2012

import urllib2
import json
import requests
import time
import glob
import os
import re
import csv

#Set up - read in api key etc.
#
#Sara-Jayne Farmer
#2012
def setup(apifile):
    apikey = ""
    if apifile <> "":
        f = open(apifile)
        apikey = f.readline().strip()
    return(apikey)


#Add datafile to a buzz dataroom
#
#Sara-Jayne Farmer
#2012
def add_file(datasetname, buzzfilename, localfile, releasenotes, apikey):
        
    user = "sara"
    baseurl = "http://buzzdata.com/api/" + datasetname

    #Create datafile container in buzz dataroom
    payload = {'api_key': apikey, 'data_file_name' : buzzfilename }
    url = baseurl + "/create_datafile"
    jsonstring = requests.post(url, params=payload).text
    jsondata = json.loads(jsonstring)
    fileuuid = jsondata["datafile_uuid"]

    #request data upload url from Buzz
    payload = {'api_key' : apikey, 'datafile_uuid' : fileuuid }
    url = baseurl + "/upload_request"
    jsonstring = requests.post(url, params=payload).text
    jsondata = json.loads(jsonstring)["upload_request"]
    uploadcode = jsondata["upload_code"]
    fileuploadurl = jsondata["url"]

    #Upload file into Buzz dataroom
    payload = {'api_key' : apikey, 'upload_code': uploadcode,
               'release_notes' : releasenotes}
    fin = open(localfile, 'rb')
    files = {'file' : (localfile, fin)}
    url = fileuploadurl
    res = requests.post(url, params=payload, files=files)
    jsonstring = res.text
    jsondata = json.loads(jsonstring)
    
    return(jsondata)



#Create a Buzz dataroom
#
#Sara-Jayne Farmer
#2012
def create_dataroom(dataroom, apikey):
    
    #Set boilerplates for datarooms
    timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())
    buzzboiler = "Data scraped from data.un.org, with columns (UNSTATS, ISO3166) added, " + \
    "containing UN and ISO3166 country codes for each row in the data, to get round " + \
    "problem of inconsistent countrynames across different UN agencies.  \nData was " + \
    "last uploaded on " + timestamp + ". \n More information about datafiles can be " + \
    "found in file dataroomindex.csv. \nOriginal source is UNdata, who should be " + \
    "cited in any distribution or duplication. "
    
    #Set parameters for dataroom
    payload = {'api_key'           : apikey,
               'dataset[name]'     : dataroom,
               'dataset[public]'   : 'true',
               'dataset[readme]'   : buzzboiler,
               'dataset[license]'  :'cc_by',
               'dataset[topics][]' : "international-development"}
    
    #Add dataroom to buzz website
    room = "sara"
    url = "http://buzzdata.com/api/" + room + "/datasets"
    jsonstring = requests.post(url, params=payload).text
    jsondata = json.loads(jsonstring)['dataset']

    print("dataroom data: ")
    print(jsondata)
    
    return(jsondata)


#Read dataset from buzz
#
#Sara-Jayne Farmer
#2012
def read_from_buzz(url, apikey):
    
    if apikey <> "":
        url = url + "/?api_key=" + apikey
    
    #Read data from buzz website
    jsonstring = urllib2.urlopen(url).read().decode("iso-8859-1")
    jsondata = json.loads(jsonstring)
    
    #Pretty-print data
    #print(json.dumps(jsondata, indent=2))
    
    return(jsondata)


#Read list of rooms in sara hive
#http://sara.buzzdata.com/api/sara/datarooms
#
#Sara-Jayne Farmer
#2012
def get_roomlist(apikey):
    
    room = "sara"
    url = "http://buzzdata.com/api/" + room + "/datasets/list"
    
    roomlist = read_from_buzz(url, apikey)
    
    return(roomlist)


#Read list of files from sara hive
#
#Sara-Jayne Farmer
#2012
def get_filelist(dataset, apikey):
    
    #Create url to send to buzz
    room = "sara"
    url = "http://buzzdata.com/api/" + room + "/" + dataset + "/list_datafiles"
    
    filelist = read_from_buzz(url, apikey)
    
    return(filelist)


#Upload datasets to sara hive
#
#Parameters: 
#* Datadir = directory containing datafiles to be uploaded
#* Masterindexcsv = csv file containing datafile details
# (blank uploaddate = please upload)
#* apifile = text file containing the user's Buzzdata api key
#
#Sara-Jayne Farmer
#2012
def upload_to_buzz(datadir, masterindexcsv, apifile):

    #Set timestamp for new uploads
    timestamp = time.strftime("%Y-%b-%d-%H-%M-%S", time.gmtime())

    #Make list of all the datafiles in the datafile directory
    datafiles = {}
    fstr = '(.+?)_(.+?)_(.+?)\.(.+?)$' #Search string for infile contents
    csvfiles = glob.glob(os.path.join(datadir, '*.csv'))
    for infile in csvfiles:

        #Grab martId and datasetId from the filename
        filename= infile[len(datadir)+1:]
        ids = re.findall(fstr, filename)
        martId    = ids[0][0]
        lenids = len(ids[0]) #There are more than two underscores in some datasetnames. Deal with it.
        dotpos = filename.rfind(".")
        scorepos = filename.rfind("_")
        if len(ids[0][2]) == (dotpos-scorepos-1):
            datasetId = ids[0][1]
        else:
            datasetId = filename[len(martId)+1:scorepos]
        datafiles[martId+"/"+datasetId] = filename        
    
    #Download details for all existing datarooms in the buzz hive
    #dataroom keys are url, public, readme, id, name
    apikey = setup("apikey.txt")
    allrooms = {}
    roomlist = get_roomlist(apikey)
    for room in roomlist:
        allrooms[room['name']] = room
    
    #Read master data.un.org index file
    #Add anything with a blank upload date to the to-upload list
    fin = open(masterindexcsv, 'rb')
    csvin = csv.reader(fin)
    masterheaders = csvin.next()

    allfiles = {}
    roomfilelists = {}
    toupload = []
    for row in csvin:
        fileid = row[0] + "/" + row[1]
        allfiles[fileid] = row
        #FIXIT: change to check file type instead
        if len(row) >= 9 and not row[0].isdigit(): #Filter out excel files
            if row[8] == "": 
                toupload += [fileid]
                print("Added " + fileid + " to upload list")
        dataroom = row[4]
        if roomfilelists.has_key(dataroom):
            roomfilelists[dataroom] += [fileid]
        else:
            roomfilelists[dataroom] = [fileid]
            
    fin.close()

    #Upload all the new files to buzz
    updatedrooms = {}
    for uploadname in toupload:

        #Add room to list of updated rooms, and create room if needed
        dataroom = allfiles[uploadname][4]
        if updatedrooms.has_key(dataroom):
            updatedrooms[dataroom] += 1
        else:
            updatedrooms[dataroom] = 1
            #If the dataroom doesn't exist, then create it.
            if not allrooms.has_key(dataroom):
                roomdetails = create_dataroom(dataroom, apikey)
                print("Created new buzz dataroom " + dataroom)
                allrooms[dataroom] = roomdetails

        datasetname = allrooms[dataroom]["id"]
        martId    = allfiles[uploadname][0]
        datasetId = allfiles[uploadname][1]
        buzzfilename = allfiles[uploadname][5]
        localfile = datadir + "/" + datafiles[martId+"/"+datasetId]
        
        #Upload the file into the dataroom
        unpage = "http://data.un.org/Data.aspx?d=" + martId + \
                 "&f=" + datasetId
        releasenotes = "File uploaded from data.un.org page " + unpage + \
        " First two columns contain GIS codes for the countrynames " + \
        "in this file, added by Sara Farmer to get round issues with " + \
        "inconsistent country names."

        add_file(datasetname, buzzfilename, localfile, releasenotes, apikey)
        print("Uploaded " + localfile + " to buzz dataset " + datasetname)
        allfiles[uploadname][8] = timestamp  
    
    #Write the corrected master index to a new file
    fout   = open("newmasterindex.csv", "wb")
    csvout = csv.writer(fout)
    csvout.writerow(masterheaders)
    for row in allfiles:
        csvout.writerow(allfiles[row])
    fout.close()
    
    #Update the dataroom index file for every dataroom that's been uploaded to
    indexreleasenotes = "Index to the files in this directory"
    for room in updatedrooms:
        indexname = "dataroomindex.csv"
        ftemp = open(indexname, "wb")
        csvtemp = csv.writer(ftemp)
        csvtemp.writerow(masterheaders)
        for fileid in roomfilelists[dataroom]:
            csvtemp.writerow(allfiles[fileid])
        ftemp.close()
        datasetname = allrooms[room]["id"]
        add_file(datasetname, indexname, indexname, indexreleasenotes, apikey)
    
    return()
