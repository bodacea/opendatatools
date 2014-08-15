#!/usr/bin/env python
''' 
HDP load from excel spreadsheet into CKAN instance datahub.io
References include:
* http://docs.ckan.org/en/ckan-2.0/api.html
* http://ckan.readthedocs.org/en/ckan-1.7.1/using-data-api.html
 
Sara-Jayne Terp, 2013
'''

from ckan_calls import *
#import pprint
import xlrd

def read_worksheet():
  return()

# Main code

#Get API key - this is listed in your CKAN account profile
fin = open("../hdpckan_api_key.txt", 'rb')
apikey = fin.read().strip()
fin.close()

#Earlier calls that worked:
#action = "action/organization_show"; data = {'id': 'hdp'}
#create_package(apikey, 'hdptestdataset')
#create_resource(apikey, 'hdptestresource', 'hdptestdataset')

#Read in excel file - dump contents out to CKAN node
wsheet_to_ckan = {"Global":"global",
                  #"Regional":"regional",
                  #problem "Country":"country",
                  #"Thematic":"thematic",
                  "Event":"event",
                  #"Disaster Type":"disastertype",
                  "Disaster Lists":"disasterlist",
                  #problem "Conflict":"conflict",
                  #"Imagery":"imagery",
                  "Physical":"physical",
                  "Conservation_Env't":"conservationandenvironmental",
                  #problem "Tabular Demographic_Statistics":"tabulardemographicstatistics",
                  #"ReferenceSystems":"referencesystems",
                  #problem "WebApps":"webapps",
                  #"USA States":"usstaterepositories",
                  #problem "Other Portals Of Interest":"otherportalsofinterest",
                  #"Live Services":"liveservices"
                  }
extra_keys = {"Global":"", "Regional":"Region", "Country":"Country",
              "Thematic":"Theme", "Event":"Event", "Disaster Type":"Disaster Type",
              "Disaster Lists":"", "Conflict":"",
              "Imagery":"", "Physical":"",
              "Conservation_Env't":"",
              "Tabular Demographic_Statistics":"Country/Region",
              "ReferenceSystems":"", "WebApps":"",
              "USA States":"State",
              "Other Portals Of Interest":"",
              "Live Services":""}

xlfile = "hdp_spreadsheet.xls"
workbook = xlrd.open_workbook(xlfile)
for wsheet in wsheet_to_ckan:
  print(wsheet)
  worksheet = workbook.sheet_by_name(wsheet)
  colnames = worksheet.row_values(0)
  nameind = colnames.index('Name')
  urlind = colnames.index('Web Address')
  logind = colnames.index('Login Required?')
  noteind = colnames.index('Notes')
  if extra_keys[wsheet] <> "":
    extraind = colnames.index(extra_keys[wsheet])
    
  for rownum in range(1,worksheet.nrows):
    row = worksheet.row_values(rownum)
    name = row[nameind]
    url = row[urlind]
    logreq = row[logind]
    if len(row)>noteind:
      notes = row[noteind]
    else:
      notes = ""
    extras = {'login_required':logreq}
    if extra_keys[wsheet] <> "":
      pluskey = row[extraind]
      extras[extra_keys[wsheet]] = pluskey    
    data = {'name':row[nameind],
            'package_id':wsheet_to_ckan[wsheet],
            'url':row[urlind],
            'notes':notes,
            'extras':extras,
            'owner_org':'datastores'}
    #print(name.encode('utf-8'))
    result = call_api(apikey, "action/resource_create", data)
  