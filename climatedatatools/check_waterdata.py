#Check waterflow data in this directory - how much real data is there, and do the filenames
#match the list of water guaging stations that we've got from VitalSigns
#Run this in direcory F) Rufiji basin water office data. 

import glob
import os
import csv

subheads = ['date', 'time', 'value', 'missingvalue', 'remarks']

#We have 2 top-level directories.  Get filenames from each of them
files = glob.glob('*')

#Do messy nasty code until get to a python manual
basins = {}
readstations = {}
for f in files:
	if f.find('.') == -1:
		#FIXIT... assumes not a directory if doesn't have a dot in name
		basins[f] = {}
		#
		substart = len(f)+1
		#Data in here is more than just txt, but pull this for now
		#Other data for later includes Met summaries in directories
		subfiles = glob.glob(os.path.join(f,'*.txt'))
		for s in subfiles:
			#Remove top-level directory name
			sname = s[substart:]
			#
			#Allow for different datatypes
			#e.g. values in automet files are in col 1; in water level col 2, in dmf col 1
			if (sname[-15:] == "water level.txt"):
				valuecol = 2
			else:
				valuecol = 1
			#print(sname)
			#
			#Check file contents - add to readstations dict
			#Record first and last times in stream, number of filled lines, % of filled lines
			minyear = 3000
			maxyear = 0
			numvalues = 0
			numlines = 0
			#
			fin = open(s, 'r')
			ls = fin.readlines() #No idea who a readline loop fails here, but it does. 
			numlines = len(ls)
			for l in ls:
				#
				#print(l)
				larray = l.split(',')
				#
				#Values
				if larray[valuecol] != "":
					numvalues += 1
					#print(larray[valuecol])
					#
					#date
					#Date is embedded here because some stations have rows for future values,
					#e.g. up to 2015.
					date = larray[0].split('-')
					if len(date) > 1:
						if int(date[2]) > maxyear:
							maxyear = int(date[2])
						if int(date[2]) < minyear:
							minyear = int(date[2])
			
			if (numvalues > 0):
				#percentfill = numvalues / numlines
				print(sname + " " + str(minyear) + 'to' + str(maxyear) + " : " + 
					str(numvalues)+ ' of ' + str(numlines))
				readstations[s] = {'minyear':minyear,'maxyear':maxyear, 'numvalues':numvalues, 
					'numlines': numlines}
			else:
				print(sname + ": empty")







