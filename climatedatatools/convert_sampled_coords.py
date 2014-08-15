import csv

fin = open('coordinates for sampled TZA and others plots in Tanzania.csv', 'rb')
fout = open('coordinates for sampled TZA and others plots in Tanzania_x.csv', 'wb')
csvin =csv.reader(fin)
csvout = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)

headernote = csvin.next() #Ignore this row - it's fluff
headers = csvin.next() #But copy the header row across
csvout.writerow(headers)

#Read in non-header rows 
for row in csvin:
	if row[1] <> "":
		plotnum = [row[1]]
	csvout.writerow(row[:1]+plotnum+row[2:])

#tidy up
fin.close()
fout.close()