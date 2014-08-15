from ckan_calls import *
import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os

  
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
#print("--CKAN data--")
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
for entry in worksheets_feed.entry:
  worksheetname = entry.title.text
  if worksheetname in sheetinfo:
    print("Processing tab "+worksheetname);
    worksheet_id = entry.id.text.rsplit('/',1)[1]
    
    #Access worksheet contents
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    for row in rows:
      for key in row.custom:
        if (row.custom[key].text <> None):
          print " %s: %s" % (key, row.custom[key].text.encode('utf-8'))
      print
