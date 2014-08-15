#
#Clean headers
#
#Example use:
#
#from cleanheaders import CleanHeaders
#c = CleanHeaders()
#
#Sara-Jayne Farmer
#2012

import csv
import glob
import os
import re
import string
import time
from Tkinter import *

#======================================================================================
#Find all headers in a directory of CSV files
#Link these headers to the index files for that directory
#
#Sara-Jayne Farmer
#2012
#======================================================================================
class CleanHeaders(Frame):
    
    Name = "CleanHeaders"
    martowners    = {} #Mart owners
    marttitles    = {} #Mart titles
    datasettitles = {} #Dataset titles
    SVindexdir    = StringVar() #Index directory
    SVdatadir     = StringVar() #Data directory

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
    #GUI version of list_headers
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def gui_list_headers(self):
        indexdir = self.SVindexdir.get()
        datadir = self.SVdatadir.get()
        print("Index dir: "+indexdir)
        print("Data dir: "+datadir)
        self.list_headers(self, indexdir, datadir)
        return()
    

    #======================================================================================
    #Put buttons etc on the GUI
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def createWidgets(self):
        self.indexdir = StringVar()
        self.datadir  = StringVar()
        self.quitButton = Button (self, text='Quit', command=self.quit)
        self.indexEntry = Entry(self, textvariable=self.indexdir)
        self.dataEntry  = Entry(self, textvariable=self.datadir)
        self.goButton = Button(self, text="Grab Headers", command=self.gui_list_headers)

        self.indexEntry.grid()
        self.dataEntry.grid()
        self.goButton.grid()
        self.quitButton.grid()
        return()


    #======================================================================================
    #
    #Sara-Jayne Farmer
    #2012
    #======================================================================================
    def stopwords():
        print("Make list of stopwords for header ontologies")
              



#======================================================================================
#Main loop
#
#Sara-Jayne Farmer
#2012
#======================================================================================

##app = CleanIndices()
##app.master.title("GIS Index Cleaner")
##app.mainloop()
