import ogr
import subprocess

inraster = 'Globcover2009_V2/GLOBCOVER_L4_200901_200912_V2.3.tif'
inshape = 'sagcot_shape/VS_Tz_Agric_SAGCOT_region.shp'

ds = ogr.Open(inshape)
lyr = ds.GetLayer(0)

lyr.ResetReading()
ft = lyr.GetNextFeature()

while ft:

    shape_name = 'SAGCOT'

    outraster = inraster.replace('.tif', '_SAGCOT.tif')
    subprocess.call(['gdalwarp', inraster, outraster, '-cutline', inshape, 
                     '-crop_to_cutline'])

    ft = lyr.GetNextFeature()

ds = None