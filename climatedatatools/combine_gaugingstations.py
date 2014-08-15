#Combine all the water guaging stations into one big file
#Do this from the CSV files that were hand-created from the shapefiles for this dataset
#FIXIT: create this file directly from the original shapefiles

import os
import glob
import csv

outfile = "../TZA_all_gauging_stations.csv"
fout = open(outfile, 'wb')
csvout = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
csvout.writerow(['basin name', 'scn', 'region name', 'location name', 
	'latitude', 'longitude', 'altitude', 'established', 'number'])

#Read in contents of each file - output them to the combined file
basincsvs = glob.glob('*.csv')

for basincsv in basincsvs:
	#
	fin = open(basincsv, 'rb')
	csvin = csv.reader(fin)
	#
	headers = csvin.next()
	#
	for r in csvin:
		if basincsv == "Internalgst.csv":
			csvout.writerow(['Internal Drainage Basin'] + r[2:7] + [r[8], r[7], r[1]])
		elif basincsv == "LTangagst.csv":
			csvout.writerow(['Lake Tanganyika Basin'] + r[1:6] + ['','',''])
		elif basincsv == "LVictoriagst.csv":
			#Split name in practice, but for now have hand-edited the imput file
			#Checking the file, can split the name on more-than-one-space (e.g. regex
			#for name1, 2+spaces, name2)
			csvout.writerow(['Lake Victoria Basin'] + r[1:6] + ['','',''])
		elif basincsv == "Nyasa_Gst.csv":
			csvout.writerow(['Lake Nyasa Basin'] + [''] + r[1:5] + ['','',''])
		elif basincsv == "Panganigst.csv":
			csvout.writerow(['Pangani Basin'] + r[2:7] + ['', '',r[1]])
		elif basincsv == "Rufijigst.csv":
			csvout.writerow(['Rufiji Basin'] + r[2:7] + ['','',r[1]])
		elif basincsv == "Rukwa_gst.csv":
			csvout.writerow(['Lake Rukwa Basin'] + r[2:7] + ['','',r[1]])
		elif basincsv == "Ruvumagst.csv":
			csvout.writerow(['Ruvuma and Southern Rivers'] + r[2:7] + ['','',r[1]])
		elif basincsv == "Wruvugst.csv":
			csvout.writerow(['Wami, Ruva and Coast'] + r[2:7] + ['','',r[1]])
		else:
			csvout.writerow(['Unknown'])

	#Couple of format errors in the resulting file, that got corrected, e.g. 
	#Lt.Ruaha instead of Lt. Ruaha. 
	fin.close()

fout.close()