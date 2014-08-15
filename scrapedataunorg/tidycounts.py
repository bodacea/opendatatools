#!/usr/bin/env python
# -*- coding: cp1252 -*-
#Pull in a csv file, and format the end of its columns
#
#Example use:
#from tidycounts import *
#histcounts()
#
#Sara-Jayne Farmer
#2012

import csv
import collections
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def tidycounts():
    #grab files
    fin = open("dataunorg_errors.csv", "rb")
    fout = open("tmp_duo_errors.csv", "wb")
    csvin = csv.reader(fin)
    csvout = csv.writer(fout)

    #Copy header row
    headers = csvin.next()
    csvout.writerow(headers)

    #Tidy data rows
    for row in csvin:
        csvout.writerow([row[0],row[1],row[2],row[3], row[4]+" ("+row[5]+")"])

    fin.close()
    fout.close()

def histcounts():
    #open count file
    fin = open("dataunorg_errors.csv", "rb")
    csvin = csv.reader(fin)

    #Ignore header row
    headers = csvin.next()

    #Count number of errors for each UNSTATS countryname
    #Ignore anything that doesn't have a UNSTATS code
    numerrors = collections.Counter()
    for row in csvin:
        if row[0] == "---":
            continue

        numerrors[row[0]] += 1

    #Create dictionary namedict[lengths][errors] = count
    namedict = {}
    for cname in numerrors:

        namelen = len(cname)
        namechar = len(cname)-len(filter(str.isalpha, cname))
        nameerror = numerrors[cname]

        if namedict.get(namelen) == None:
            namedict[namelen] = {}
        if namedict[namelen].get(nameerror) == None:
            namedict[namelen][nameerror] = 0
        namedict[namelen][nameerror] += 1
        
    #Create vectors for the plot
    namelens = []
    namecounts = []
    nameerrors = []
    for namelen in sorted(namedict.keys()):
        for nameerror in sorted(namedict[namelen].keys()):
            namelens = namelens + [namelen]
            nameerrors = nameerrors + [nameerror]
            namecounts = namecounts + [namedict[namelen][nameerror]*2]

    #Set up plotting canvas. Matplotlib code is from
    #http://www.prettygraph.com/blog/how-to-plot-a-scatter-plot-using-matplotlib/
    fig = plt.figure(figsize=(6,6))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_title("GIS Error Counts in data.un.org",fontsize=14)
    ax.set_xlabel("Name length (characters)",fontsize=12)
    ax.set_ylabel("Number of name variations",fontsize=12)
    ax.grid(True,linestyle='-',color='0.75')
    
    #Plot namelengths against number of errors
#    ax.scatter(namelens,nameerrors,s=20,color='tomato'); #Use s=vector for bubblesize
    ax.scatter(namelens,nameerrors,c=namecounts,s=20); #Use s=vector for bubblesize
#    ax.scatter(namechars,nameerrors,s=20,color='blue');
    plt.show()
    canvas.print_figure('name_errors.png',dpi=500)



            
