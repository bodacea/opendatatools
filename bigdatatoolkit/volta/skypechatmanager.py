'''
Python code to manage saved Skypechat data, i.e. doesn't need a Skypechat
connection.

Deals with 3 different Skype data sources:

* Skype API outputs - these are .csv files
* Skype cut-and-paste outputs - these are .txt files
* Skype CSV files. These are output by cut-and-paste converter, and are
  deliberately in same format as the Skype API outputs. 

Example use:
from skypechatmanager import *
read_skypemessages_cutpaste("testskype.txt", "testskype.csv", N)

Sara-Jayne Farmer
2012
'''

import csv
import nltk
import re
import time
import networkx as nx
import datetime


'''
Read in cut-and pasted skypechat file. File is a text document.
Split into array of messages, where each message vector is [from,body,timestamp,event]
This matches the output from the Skype API, i.e. looks like: 
 [Noel,Sara Farmer,11/2/2012/15:56:24,ADD]
 [joy,this could be useful,11/2/2012/3:56:32,SAID]
Output this data to a .csv file, if outfile is set in the input parameters

FIXIT: If a comment is from the same person and multi-line at the same time, then add
the comments together? 

Sara-Jayne Farmer
2012
'''
def read_skypemessages_cutpaste(infile="", outfile="", verbose="N"):

    #Get infile from user if it isn't in the parameters list
    if infile == "":
        infile = raw_input("Input filename: ")
    fin = open(infile, 'rb')

    #Only output to file if it's asked for
    if outfile != "":
        fout = open(outfile, "wb")
        csvout = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)

    skypemessages = []
    datestr     = '\[(.+?)/(.+?)/(.+?) (.+?):(.+?):(.+?) (.+?)\]'
    m_timestamp = "" #to deal with emoticons on their own line problem.
    m_from      = ""#to deal with emoticons on their own line problem.
    for line in fin:
        line = line.strip() #Remove \r\n junk from end of line
        if verbose != "N":
            print(line)

        #remove date portion of line
        #Expect it in form "m/d/y h:m:s xx" where xx is "AM" or "PM"
        timedata = re.findall(datestr + ' (.+?)$', line)

        #Deal with emoticons, which appear on lines on their own
        if len(timedata) == 0:
            #Use the last person and timestamp details
            outrow = [m_from, line, m_timestamp, "SAID"]
            skypemessages += [outrow]
            if outfile != "":
                csvout.writerow(outrow)
            continue
        
        mtime = timedata[0][:-1]
        addtime = 0
        if mtime[3] == "12": #12 pm is lunchtime, 12am is midnight
            addtime += -12
        if mtime[6] == "PM": #Convert to 24-hour clock by adding 12 to pm - except 12pm
            addtime += 12

        #Datetime format is (y,m,d,h,m,s)
        #Skype uses epoch time, i.e. time since Jan 1st 1970.
        dt = datetime.datetime(int(mtime[2]), int(mtime[0]), int(mtime[1]), 
                               int(mtime[3])+addtime, int(mtime[4]), int(mtime[5]))
        m_timestamp = time.mktime(dt.timetuple())
        
        #print(timedata)
        mdata = timedata[0][-1:][0]

        #Strip and reformat sender, message etc.
        #FIXIT: deal with xxx "removed" YYY messages
        cols = re.findall("\*\*\* (.+?) (has left|added (.+?)) \*\*\*$", mdata)
        if cols != []:
            m_from = cols[0][0]
            #Found added, has left etc - treat differently
            if cols[0][1] == "has left":
                m_type = "HASLEFT"
                m_body = ""
            else:
                m_type = "ADDEDMEMBERS"
                m_body = cols[0][2]
        else:
            cols = re.findall("\*\*\* (.+?) removed (.+?) from this conversation. \*\*\*$", mdata)
            if cols != []:
                m_from = cols[0][0]
                m_type = "REMOVEDMEMBERS"
                m_body = cols[0][1]

            else:
                #Found text line -extract date, time, person and text
                cols = re.findall('(.+?): (.+?)$', mdata)
                if cols == []: #No message, just username
                    m_from = mdata[:-2]
                    m_type = "SAID"
                    m_body = ""
                else: #Username and message
                    m_from = cols[0][0]
                    m_type = "SAID"
                    m_body = cols[0][1]

        #write cols out to a CSV file
        outrow = [m_from, m_body, m_timestamp, m_type]
        skypemessages += [outrow]
        if outfile != "":
            csvout.writerow(outrow)

    if outfile != "":
        fout.close()

    return(skypemessages)


'''
Read in Skypechat held in csv form
Assume that data is in columns:
datetime, "said", text
datetime, "added", person1, person2 (person1 added person2)
datetime, "hasleft", person1

Sara-Jayne Farmer
2012
'''
def read_skypemessages_csv(csvfile):

    fin = open(csvfile, 'rb')
    csvin = csv.reader(fin, quoting=csv.QUOTE_NONNUMERIC)
    headers = csvin.next()

    skypemessages = []
    for row in csvin:
        skypemessages += [row]
    return(skypemessages)


'''
Read in list of Skypechat users held in csv form
Assume that data is in columns:
skypename, listed name, numcontacts, location, country
and has a header row

Sara-Jayne Farmer
2012
'''
def read_skypeusers_csv(csvfile):

    fin = open(csvfile, 'rb')
    csvin = csv.reader(fin, quoting=csv.QUOTE_NONNUMERIC)
    headers = csvin.next()

    skypeusers = {}
    for row in csvin:
        skypeusers[row[0]] = {}
        skypeusers[row[0]]["skypename"] = row[1]
        skypeusers[row[0]]["numcontacts"] = row[2]
        skypeusers[row[0]]["location"] = row[3]
        skypeusers[row[0]]["country"] = row[4]

    fin.close()
    return(skypeusers)

'''
Profile skypechat contributors

Sara-Jayne Farmer
2012
'''
def count_countributions(skypemessages):
    
    #Count contributions to chat
    cnt = Counter()
    for m in skypemessages:
        cnt[m.FromDisplayName] += 1

    print("Messages: "+ str(len(skypemessages)) + " writers: " + str(len(cnt)))
    return(cnt)


'''
Profile skypechat member locations

Sara-Jayne Farmer
2012
'''
def count_locations(skypemembers):
    
    #Count contributions to chat
    countries = Counter()
    cities = Counter()
    timezones = Counter()
    for skypeid in skypemembers:
        countries[members[skypeid][Country]]  += 1
        cities[members[skypeid][City]]        += 1
        timezones[members[skypeid][Timezone]] += 1

    print("Countries: "+ str(len(countries)) + " cities: " + str(len(cities)))
    return([countries, cities, timezones])


'''
Analyse Skypechat files

Sara-Jayne Farmer
2012
'''
def analyse_skypechatfiles(messagesfile, usersfile):
    
    #Pull in data from files, if requested
    if messagesfile != "":
        skypemessages = read_skypemessages_csv(messagesfile)
    if userssfile != "":
        skypeusers = read_skypeusers_csv(usersfile)

    #Call skype analyser
    userstats, addgraph, texthist = analyse_skypechat(skypemessages, skypeusers)

    return()


'''
Analyse Skypechat

Sara-Jayne Farmer
2012
'''
def analyse_skypechat(skypemessages, skypeusers):

    #Look at user contributions to this chat
    nltkstops = nltk.corpus.stopwords.words('english')
    chatwords = []
    userstats = {}
    addgraph = nx.DiGraph()
    allwords = r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*"
    for row in messages:
        #Add line to chat string
        person    = row[0]
        text      = row[1].lower()
        timestamp = row[2]
        action    = row[3]
        
        if not users.has_key(person):
            userstats[person] = {}
            userstats[person]["contributions"] = 0
            
        if action not in ["ADDEDMEMBERS", "HASLEFT"]:
            #Tokenise text into words, and add them to chatstring list
            #DETAIL: each word is only counted *once* per message.
            #Output isn't number of times a word is used, but number of
            #messages that a word is used in. #subtle!
            #FIXIT: remove non-alphanumerics from the list
            foundwords = re.findall(allwords, text)
            chatwords = chatwords + list(set(foundwords).difference(nltkstops))
            userstats[person]["contributions"] += 1
        else:
            if action == "ADDEDMEMBERS":
                userstats[person]["added"] = [text, timestamp]
            else: #HASLEFT
                userstats[person]["left"] = [timestamp]

    
    #Display a graph of the user adds, i.e. from->to
    #A dendrogram would be nice too
    for person in users.keys():
        if userstats[person].has_key("added"):
            addgraph.add_edge(userstats[person]["added"][0], person,
                       {"timestamp" : userstats[person]["added"][1]})


    #Get word histogram from text
    #Remove stopwords and names, and do wordle of the remainder
    #Might need to keep a list of people's names for this
    print("Most common words used: ")
    texthist = nltk.FreqDist(chatstring)
    for token in sorted(texthist.keys()[:20]):
        print(token + " " + str(texthist[token]) + "times")

    return userstats, addgraph, texthist

