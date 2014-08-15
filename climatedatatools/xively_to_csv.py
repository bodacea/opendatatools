import csv
import json

fin = open("TZA_xively.json", 'rb')
fout = open("TZA_xively.csv", 'wb')
csvout = csv.writer(fout, , quoting=csv.QUOTE_NONNUMERIC)

data = json.loads(fin.read())

headers = []
csvout.writerow(headers)

for i in data['results']:
	//Convert data['results'][i] into array. Dump to CSV.


fin.close()
fout.close()