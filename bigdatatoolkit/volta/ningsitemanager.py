#Convert Ning output from Json to csv
#Ning output (groups, members, events) created by ning superadmin using
#the ning tool NingNetworkArchiver
#
#Code to read Ning json files and convert them to csv for ordinary mortals to
#read (Ning's json messes up python).
#
#Example use:
#
#from ningmanager import *
#ningjsontoexcel("yourfilename.json", "member")
#Second value is the type: one of "group", "member", "event"
#
#Sara-Jayne Farmer 
#2012

import xlwt
import json
import os
import re
import time
import xlrd
import nltk

#Convert any apostrophes etc in the text into json-readable form
#(Python is stricter on json format than most)
#From http://stackoverflow.com/questions/8011692/valueerror-in-decoding-json
def asciirepl(match):
    return '\\u00' + match.group()[2:]
   

#Get json contents from json file produced by Ning, which are *not* in pure json format,
#and get rejected by the (rather strict) Python Json readers
#
#Sara-Jayne Farmer
#2012
def import_ning_json(jsonfile, ningtype):

    #Get Ning data from file
    fin = open(jsonfile)
    ff = fin.read()
    fin.close()
    
    #Put Ning data into Python-readable json format
    if ningtype == "member":
        offset = 2
    else:
        offset = 1
    correcteddata = '{"' + ningtype + '":' + ff[1:len(ff)-offset] + "}"
    p = re.compile(r'\\x(\w{2})')
    ascii_string = p.sub(asciirepl, correcteddata)

    #Load corrected text into json
    data = json.loads(ascii_string)
    jsonkeys = data.keys() #data is a dictionary
    listtype = jsonkeys[0]
    dataset = data[listtype] #dataset is an array of entities: groups, members, etc.

    return(dataset)

#Get json contents from json file produced by Ning, where that file is long and
#the json reader keeps declaring it corrupt, with messages like
#"Expecting , delimiter: line 1 column 530617"
#This happens a lot with long lists of members. 
#
#Sara-Jayne Farmer
#2012
def import_ning_json_long(jsonfile, ningtype):
    
    #Get Ning data from file
    fin = open(jsonfile)
    ff = fin.read()
    fin.close()

    #Put Ning data into Python-readable json format
    if ningtype == "member":
        offset = 2
    else:
        offset = 1
    correcteddata = '{"' + ningtype + '":' + ff[1:len(ff)-offset] + "}"
    p = re.compile(r'\\x(\w{2})')
    ascii_string = p.sub(asciirepl, correcteddata)

    #Split data up into sections
    dataset = {}
    records = ascii_string.split('{"createdDate":')
    for r in range(1,len(records)-1):

        #Deal with really wierd Ning bug where they don't put commas between some of
        #the member records. 
        if records[r][-1:] == "," or records[r][-1:] == "]":
            userecord = records[r][:-1]
        else:
            userecord = records[r]
        
        #print("Record " + str(r))
        #print('{"createdDate":' + userecord)
        d = json.loads('{"createdDate":' + userecord)
        dataset[r] = d

    #Handle last record in the set, which has extra json characters in it
    #print('{"createdDate":' + records[len(records)-1][:-1])
    d = json.loads('{"createdDate":' + records[len(records)-1][:-1])
    dataset[len(records)-1] = d
    
    return(dataset)


#Convert json file contents to excel
#Expects 3 different input files in ning json format: members, groups, events
#But will ignore a file if the user doesn't enter a filename for it
#Files come in either as a parameter (filelist) or direct from the UI (if filelist is empty)
#
#Sara-Jayne Farmer
#2012
def ningjsontoexcel(filelist=None):

    #Get list of json files from parameter or directly from user
    if filelist is None:
        memfile = raw_input("JSON file containing members data: ")
        grpfile = raw_input("JSON file containing groups data: ")
        evtfile = raw_input("JSON file containing events data: ")
    else:
        memfile = filelist[0]
        grpfile = filelist[1]
        evtfile = filelist[2]

    #Create excel workbook. Add a front sheet to it, to summarise the conversion
    wbk = xlwt.Workbook()
    frontsheet = wbk.add_sheet("Summary", cell_overwrite_ok=True)
    frontsheet.write(0,0, "Ning database summary")
    frontsheet.write(1,0, "Created " + time.asctime(time.gmtime()) + " GMT")
    frontsheet.write(2,0, "From members file :" + memfile)
    frontsheet.write(3,0, "And groups file :" + grpfile)
    frontsheet.write(4,0, "And events file :" + evtfile)

    
    #Get data from Members file
    #Member dataset is a dictionary with keys:
    #(createdDate, fullName, birthdate, email, profileQuestions, profilePhoto, level, state,
    #contributorName)
    #profileQuestions is also a dictionary, with keys:
    #(Organization/Affiliation, E-Mail, SkypeID, Twitter handle, Bio, What is your previous experience
    #with the Ushahidi platform..., If you worked on a Ushahidi..., Which teams would you like to join...,
    #What specific skills..., What languages..., What is your location and time zone...
    if memfile != "":
        print("Adding data from members file")
        dataset = import_ning_json_long(memfile, "member")
        memsheet = wbk.add_sheet("MemberSummary", cell_overwrite_ok=True)

        #Create keylist (aka column headings) for the dataset
        #Create set containing all the keys
        datakeyset = set()
        dictkeys = set()
        listkeys = set()
        for member in dataset:
            memkeys = set(dataset[member].keys())
            newkeys = memkeys.difference(datakeyset)
            
            #Unpack nested keys - only to 1 level down though.
            addkeys = newkeys.copy()
            for k in newkeys:
                if type(dataset[member][k]) == dict:
                    dictkeys.add(k)
                    addkeys.remove(k) #don't do this, or will always be nesting
                    for i in dataset[member][k].keys():
                        addkeys.add(k + ":" + i) #Preface keyname, to avoid conflicts, e.g. email vs questions:email
                else:
                    if type(dataset[member][k]) == list:
                        #Aaargh! Comments problem again - just ignore them!
                        #Design decision - do *not* output comments on member pages to file
                        listkeys.add(k)
                    
            datakeyset = datakeyset.union(addkeys)
        for key in dictkeys.union(listkeys):
            datakeyset.remove(key)
        
        #Create list of column numbers for each datakey
        keycols = {}
        col = 0
        for key in datakeyset:
            keycols[key] = col
            memsheet.write(0, col, key)
            col += 1
        
        #Add each member to the datasheet
        mrow = 1
        for member in dataset:
            for key in dataset[member].keys():
                if key in dictkeys:
                    print("writing out data with key: " + key)
                    print(dataset[member][key])
                    #write out all the subkeys
                    if dataset[member][key] != []: #Yes, we have some empty profile sets!
                        for subkey in dataset[member][key].keys():
                            memsheet.write(mrow, keycols[key + ":" + subkey],
                                           dataset[member][key][subkey])
                else:
                    if key not in listkeys:
                        #print("writing out data with key: " + key)
                        #print(dataset[member][key])
                        memsheet.write(mrow, keycols[key], dataset[member][key])
            mrow += 1
            

    #Get data from Groups file
    #Group data format: dataset is a dictionary with keys:
    #(description, title, memberCount, contributorName, approved, allowInvitations, updatedData,
    #groupPrivacy, url, members, createdDate, allowMemberMessaging, id)
    #Group: dataset['members'] is an array
    #Group: dataset['contributorName'] is an array
    #Want csv file that looks like:
    #key1,value
    #key2,value
    #members,value1,details1
    #members,value2,details2
    #...
    #contributorName,value1, details1
    #contributorName,value2, details2
    #...
    if grpfile != "":
        print("Adding data from groups file")
        dataset = import_ning_json(grpfile, "group")

        sumsheet = wbk.add_sheet('GroupSummary', cell_overwrite_ok=True) #Add summary sheet to workbook
        grow = 1   #Group's row in the CSV worksheet "summary"
        keycols = [] #Ordered list of all columns in the CSV worksheet "summary"
        listkeys = [] #List of all the keys that do *not* go into the CVS worksheet "summary"

        #loop around each group
        for group in dataset:

            #Get keys for this group
            #NB different groups have different sets of keys.
            groupkeys = group.keys()

            #Add new keys to the CVS worksheet 'summary' and to the list of CSV worksheet columns
            for key in groupkeys:
                
                #Don't put lists onto the summary page.
                if type(group[key]) == type(list()):
                    listkeys += [key]

                else:
                    #Write new key to worksheet header and put into keycols array
                    if (key in keycols) == False:
                        keycols = keycols + [key]
                        sumsheet.write(0,len(keycols)-1,key)
                        
                    col = keycols.index(key)
                    sumsheet.write(grow, col, [group[key]])

            #Convert contributorName from code to member's full name  
            cn = group['contributorName']
            initiator = cn #if we can't find the initiator, record the code instead
            
            #Print out list keys
            sheetname = group['url']
            sheetname = sheetname[:min(31,len(sheetname))] #Excel limits name to 31 chars
            groupsheet = wbk.add_sheet(sheetname, cell_overwrite_ok=True)
            prow = 1
            pkeys = []
            for person in group['members']:
                for pkey in person.keys():
                    if (pkey in pkeys) == False:
                        pkeys = pkeys + [pkey]
                        groupsheet.write(0,len(pkeys)-1,pkey)
                    pcol = pkeys.index(pkey)
                    groupsheet.write(prow,pcol,[person[pkey]])
                prow = prow+1

                #Check for group initiator's code
                if person['contributorName'] == cn:
                    col = keycols.index('contributorName')
                    sumsheet.write(grow, col, person['fullName'])
                
            grow = grow + 1

    #Get date from Events file
    #Event dataset is a dictionary with keys:
    #()
    if evtfile != "":
        print("Adding data from events file")
        dataset = import_ning_json(evtfile, "event")

        
    #Save the new Excel workbook to a file
    wbk.save("ning_data.xls")
    
    return ()

#Analyse excel file for things like languages (SBTF-specific)
#
#Sara-Jayne Farmer
#2012
def analyse_excel(excelfile):

    #Pull in file data
    book = xlrd.open_workbook(excelfile)

    #Grab and analyse members data
    langstopwords = ["excellent", "fluent", "proficient", "intermediate",
                     "conversational"]
    knownlangs = ["english", "french", "arabic", "german"]
    if "MemberSummary" in book.sheet_names():
        memsheet = book.sheet_by_name("MemberSummary")
        headings = memsheet.row_values(0)
        langtext = "profileQuestions:What languages do you speak and your level of proficiency?"
        if langtext in headings:
            langindex = headings.index(langtext)
            langdata = memsheet.col_values(langindex)[1:]
            langtext = ' '.join(w for w in langdata) #Make one long string
            langwords = re.compile(r'[^A-Z^a-z]+').split(langtext.lower())
            fd = nltk.FreqDist(langwords)
fout = open("langwords.csv", "wb")
csvout = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
csvout.writerow(["Word", "Frequency"])
for key in fd.keys():
    csvout.writerow([key, fd[key]])
fout.close()
            
            

    
