#!/usr/bin/env python
# -*- coding: cp1252 -*-

#This program contains small functionsa to analyse text files
#
#Example use:
#
#from analysetext import *
# [cs, cons] = summarise_skypechat("../data/skypechats/skypechat_SBTF General Chat Room.csv")
#
#Sara-Jayne Farmer
#2012

import nltk
import csv
import re


#======================================================================================
#Compare two stopword lists
#
#Sara-Jayne Farmer
#2012
#======================================================================================
def compare_stopwords(infile):

    stops = {}

    #Import nltk stopword list
    nltkstops = nltk.corpus.stopwords.words('english')
    for stop in nltkstops:
        stops[stop.lower()] = "nltk"

    #Import file stopword list
    fin = open(infile)
    for line in fin:
        stop = line.strip().lower()
        if stops.has_key(stop) and stops[stop] == "nltk":
            stops[stop] = "both"
        else:
            stops[stop] = "file"
    fin.close()
    
    #Dump to file
    fout = open("stopwordlists.csv", 'wb')
    csvout = csv.writer(fout)
    for stop in sorted(stops.keys()):
        csvout.writerow([stop, stops[stop]])
    fout.close()
            
    return(stops)
