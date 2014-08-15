#!/usr/bin/env python
''' 
HDP load from excel spreadsheet into CKAN instance datahub.io
References include:
* http://docs.ckan.org/en/ckan-2.0/api.html
* http://ckan.readthedocs.org/en/ckan-1.7.1/using-data-api.html
 
Sara-Jayne Terp, 2013
'''

from ckan_calls import *
import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re
import os

def connect_to_googledoc(googleuser, googlepass, googledoc):
  
  # Connect to Google
  gd_client = gdata.spreadsheet.service.SpreadsheetsService()
  gd_client.email = googleuser
  gd_client.password = googlepass
  gd_client.ProgrammaticLogin()
  
  #Get spreadsheet and worksheet IDs.
  q = gdata.spreadsheet.service.DocumentQuery()
  q['title'] = googledoc
  q['title-exact'] = 'true'
  spreadsheet_feed = gd_client.GetSpreadsheetsFeed(query=q)
  spreadsheet_id = spreadsheet_feed.entry[0].id.text.rsplit('/',1)[1]
  worksheets_feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
  
  return(gd_client, spreadsheet_id, worksheets_feed)

#Read in google keys and connect to Google
[ckankeys, googlekeys] = read_keys("../hdpckan_keys.txt")
[gd_client, spreadsheet_id, worksheets_feed] = connect_to_googledoc(googlekeys['user'], 
  googlekeys['pass'], googlekeys['doc'])

#Find the "CKAN" worksheet in googledoc - get data from it
print("--Reading CKAN info from spreadsheet--")
for entry in worksheets_feed.entry:
  if (entry.title.text == "CKAN Info"):
    worksheet_id = entry.id.text.rsplit('/',1)[1]
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    sheetinfo = {}
    for row in rows:
      rowname = row.custom['googledoctabname'].text
      sheetinfo.setdefault(rowname, {})     
      for key in row.custom:
        sheetinfo[rowname].setdefault(key, row.custom[key].text)
    break
#print(sheetinfo)

#Process each worksheet in turn
print("--Spreadsheet Tabs--");
owner_id = 'datastores'
defaultdata = {'name':'','webaddress':'','notes':'', 'loginrequired':''}
for entry in worksheets_feed.entry:
  worksheetname = entry.title.text
  if worksheetname in sheetinfo:
    print("Processing tab "+worksheetname);
    worksheet_id = entry.id.text.rsplit('/',1)[1]
    package_id = sheetinfo[worksheetname]['ckanpackage']
    
    #Create new CKAN package for this worksheet
    try: 
      result = create_ckan_package(ckankeys['url'], ckankeys['apikey'], 
                                   package_id, owner_id)
    except:
      print("Error creating package "+package_id)
    
    #Create new CKAN resources from worksheet contents
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    for row in rows:
      #convert googlespreadsheet row into dict - there must be a better way...
      rowdata = {}
      for key in row.custom:
        if (row.custom[key].text <> None):
          rowdata.setdefault(key, row.custom[key].text)
          #print " %s: %s,%s" % (key, row.custom[key].text.encode('utf-8'), rowdata[key].encode('utf-8'))
      
      #Create CKAN data package from the dictionary
      for i in defaultdata.keys():
        rowdata.setdefault(i, defaultdata[i])
      data = {'url':rowdata['webaddress'],
              'notes':rowdata['notes']}
      resource_id= rowdata['name']
      extras = {'login_required':rowdata['loginrequired']}
      for i in (rowdata.viewkeys() - defaultdata.viewkeys()):
        extras.setdefault(i, rowdata[i])
      data['extras'] = extras  
      print("Creating resource "+resource_id.encode('utf-8'))
      
      try: 
        result = create_ckan_resource(ckankeys['url'], ckankeys['apikey'], data,
                                      resource_id, package_id, owner_id)
      except:
        print("Error creating resource "+rowdata['name'].encode('utf-8'))
      print


