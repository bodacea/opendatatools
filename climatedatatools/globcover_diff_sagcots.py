#Read geotiff file containing Globcover data for the SAGCOT region of 
#Tanzania, and create a new layered map with bands:
# 1: original data
# 2: 11 or 14 to another use
# 3: another use to 11 or 14
# 4: Stable 11 or 14
# 5: 50 to another use
# 6: another use to 50
# 7: stable 50

import sys
import gdal
from   gdalconst import *
import struct
from PIL import Image
import csv

#Set area filenames
infile1 = "GlobcoverTZA_SAGCOT2004.tif"
infile2 = "GlobcoverTZA_SAGCOT2009.tif"


#Open and check raster files
#Should be 1 band, GeoTIFF, WGS84
dataset1 = gdal.Open(infile1, GA_ReadOnly)
dataset2 = gdal.Open(infile2, GA_ReadOnly)
#geoTransform1 = dataset1.GetGeoTransform() 
cols1 = dataset1.RasterXSize
cols2 = dataset1.RasterXSize
rows1 = dataset1.RasterYSize
rows2 = dataset1.RasterYSize
xSize = max(cols1, cols2)
ySize = max(rows1,rows2)

#Output to new raster file
#newGeoTrans = list(geoTransform)
#newGeoTrans[0] = 0
#newGeoTrans[3] = maxY

d1band = dataset1.GetRasterBand(1)
d2band = dataset2.GetRasterBand(1)

#Layer datasets using http://www.gdal.org/gdalbuildvrt.html ?
outfile = "GlobcoverTZA_SAGCOTdiff.tif"
#usetypes = [11, 14]
usetypes = [50]
frast = open(outfile, 'wb')
im = Image.new("RGB", (xSize,ySize))
totchanges = 0
totfill = 0
datahist1 = {}
datahist2 = {}
for y in range(0, ySize):
	scanline1 = d1band.ReadRaster(0,y, xSize,1, xSize,1, GDT_Float32)
	scanline2 = d2band.ReadRaster(0,y, xSize,1, xSize,1, GDT_Float32)
	row1f = struct.unpack('f' * xSize, scanline1)
	row2f = struct.unpack('f' * xSize, scanline2)
	row1 = [int(i) for i in row1f]
	row2 = [int(i) for i in row2f]

	for x in range(0, xSize):

		datahist1.setdefault(row1[x],0)
		datahist1[row1[x]] += 1
		datahist2.setdefault(row2[x],0)
		datahist2[row2[x]] += 1

		if (row1[x] != 0):
			totfill += 1
			if (row1[x] != row2[x]):
				totchanges += 1
			if row2[x] != 0:
				in1 = (row1[x] in usetypes)
				in2 = (row2[x] in usetypes)
				if in1 and in2: # same
					im.putpixel((x,y), (255,255,255))
				elif in1 and not(in2): # loss
					im.putpixel((x,y), (255,0,0))
				elif not(in1) and in2: # gain
					im.putpixel((x,y), (0,204,0))
				else: #anything else
					im.putpixel((x,y), (0,0,0))
			else:
				im.putpixel((x,y), (255,255,255))
		else:
			im.putpixel((x,y), (255,255,255))

print("total changes: "+ str(100.0*totchanges/totfill)+ " %")
im.save("outimage.png")
frast.close()

#Send histogram to file
histkeys = sorted(list(set(datahist1.keys() + datahist2.keys())))
histfile = "Globcover_hist.csv"
fcsv = open(histfile, 'wb')
csvout = csv.writer(fcsv, quoting=csv.QUOTE_NONNUMERIC)
csvout.writerow(["filename"] + histkeys)
histrow1 = [infile1]
histrow2 = [infile2]

for i in histkeys:
	if datahist1.has_key(i):
		histrow1 += [datahist1[i]]
	else:
		histrow1 += ['']

	if datahist2.has_key(i):
		histrow2 += [datahist2[i]]
	else:
		histrow2 += ['']

csvout.writerow(histrow1)
csvout.writerow(histrow2)
fcsv.close()

# print("Hist 2004")
# for i in sorted(datahist1.keys()):
# 	print(str(i) + ":" + str(datahist1[i]))

# print("Hist 2009")
# for i in sorted(datahist2.keys()):
#  	print(str(i) + ":" + str(datahist2[i]))
