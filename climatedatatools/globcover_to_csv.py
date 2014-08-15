#Read geotiff file containing Globcover data for the world, extract data for 
#Tanzania and output it in csv, a format that dataviz people can read easily
#Superceded by using gdalwarp with the SAGCOT shapefile.

import sys
import gdal
from gdalconst import *
import csv
import struct

def latlongtoPixel(geoMatrix, lat, lon):
	ulX = geoMatrix[0]
	ulY = geoMatrix[3]
	xDist = geoMatrix[1]
	yDist = geoMatrix[5]
	rtnX = geoMatrix[2]
	rtnY = geoMatrix[4]
	pixelx = int((lat - ulX) / xDist)
	pixely = int((ulY - lon) / xDist)
	return(pixelx, pixely)


#Get bounding box from country shapefile
#E.g. countryshp = "TZA_boundingbox.shp"
def getcountrybounds(shpfile):
	shapef = ogr.Open(shpfile)
	lyr = shapef.GetLayer(os.path.split(os.path.splitext(shpfile)[0])[1])
	poly = lyr.GetNextFeature()
	minX, maxX, minY, maxY = lyr.GetExtent()
	return(minX, maxX, minY, maxY)

#from https://gist.github.com/stefanocudini/5201689
def pt2fmt(pt):
	fmttypes = {
		GDT_Byte: 'B',
		GDT_Int16: 'h',
		GDT_UInt16: 'H',
		GDT_Int32: 'i',
		GDT_UInt32: 'I',
		GDT_Float32: 'f',
		GDT_Float64: 'f'
		}
	return fmttypes.get(pt, 'x')
 

#Set geotiff filename
filename = "Globcover2009_V2/GLOBCOVER_L4_200901_200912_V2.3.tif"
#filename = "Globcover_V2/GLOBCOVER_200412_200606_V2.2_Global_CLA.tif"

#Set TZA bounding box - use TZA_boundingbox shapefile numbers
minX = 29.399
maxX = 40.561523
minY = -0.922812
maxY = -12.039

#Open and check raster file
#Should get cols 129600, rows 55800, bands 1, driver GeoTIFF, WGS84
dataset = gdal.Open(filename, GA_ReadOnly)
cols = dataset.RasterXSize
rows = dataset.RasterYSize
bands = dataset.RasterCount
driver = dataset.GetDriver().LongName
proj = dataset.GetProjectionRef()
print(str(rows) + "," + str(cols) + " [rows,cols] on " + str(bands) 
	+ " bands with driver: " + driver)

#0: top left x, 1: w-e pixel res, 2:rotation (0 = north up), 
#3: top left y, 4: rotation, 5:n-s pixel res
geoTransform = dataset.GetGeoTransform() 

ulX, ulY = latlongtoPixel(geoTransform, minX, maxY)
lrX, lrY = latlongtoPixel(geoTransform, maxX, minY)
print("x,y size: "+ str(lrX - ulX) + "," + str(ulY-lrY) )
print(str(ulX) + "," + str(lrX))
print(str(lrY) + "," + str(ulY))

#Now cut out the pixels we want, and add them to a nice big csv file
xOffset = ulX
yOffset = ulY
xSize = lrX - ulX
ySize = ulY - lrY

#Output pixels to new raster file too - not doing this bit this time
newGeoTrans = list(geoTransform)
newGeoTrans[0] = minX
newGeoTrans[3] = maxY

band = dataset.GetRasterBand(1)
bandtype = gdal.GetDataTypeName(band.DataType)
btype = band.DataType
fmt = pt2fmt(btype)
print(bandtype)

csvoutfile = "GlobcoverTZA.csv"
fcsv = open(csvoutfile, 'wb')
rasteroutfile = "GlobcoverTZA.tif"
frast = open(rasteroutfile, 'wb')
csvout = csv.writer(fcsv, quoting=csv.QUOTE_NONNUMERIC)
for y in range(lrY,ulY):
	scanline = band.ReadRaster(ulX,y, xSize,1, xSize,1, GDT_Float32)
	row = struct.unpack('f' * xSize, scanline)
	csvout.writerow([int(i) for i in row])

fcsv.close()
frast.close()
