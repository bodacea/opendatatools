"""
Grab messages from a named Skype chat, using Skype4Py from a Linux PC

Example use:

from skypechatconnector import *

s = SkypechatConnector()
i = s.get_chatroom("Ushahidi Dev Chat")
s.getroomslike("USAID")
s.dump_messages(i)
s.profile_writers(i)

Sara-Jayne Farmer 
2012
"""

import Skype4Py
from collections import Counter
import csv
import os
import re
import string


#Produce time-sorted list
def message_timestamp_cmp(x, y):
    return int(x.Timestamp - y.Timestamp)


#Class to handle Skype chats
#Sara-Jayne Farmer
#2012
class SkypechatConnector:
    
    name = "SkypechatConnector" #Class name
    sconn = ''                  #Skype connection
    chats = ""                  #Chats
    mlist = ""                  #Message list
    
    
    #Initialise Skype link
    def __init__(self):
        print("Setting up link to Skype")

        #Set up Skype
        #Need to have Skype running first, then click on "allow to access skype"
        #message in there when this program starts
        if os.name == "nt":
            print("Windows")
            #32 bit and 64 bit windows behave differently with Skype
            if 'PROGRAMFILES(X85)' in os.environ:
                self.sconn = Skype4Py.Skype() #64-bit
            else:
                self.sconn = Skype4Py.Skype() #32-bit
        elif os.name == "os2":
            print("Mac")
            self.sconn = Skype4Py.Skype()
        else:
            print("Linux machine or similar")
            self.sconn = Skype4Py.Skype(Transport='x11')

        self.sconn.FriendlyName = "Skype_chat_trawler"
        self.sconn.Attach()
        

    #Make friends with lots of people at once
    def make_buddies(self, userids, message):
        for userid in userids:
            u = self.sconn.User(userid)
            if u.BuddyStatus < 2: #Not friends, or unknown, or ex-friend
                u.SetBuddyStatusPendingAuthorization(message)
                print("Sent buddy request to "+ userid)
        return()
    
    
    #Create a chatroom
    def create_chatroom(self, chatname, userids):

        #Create chatroom in Skype, with the given list of users
        self.sconn.CreateChatWith(userids)

        #Chat.addmembers also useful
        #And need to name the chat, set topic etc.
        #NB might be easier to create a group, then a chat for the group
        
        
        return()


    #Find all chatrooms with a given string in their name
    def getroomslike(self, chatname):
        
        roomslike = []
        self.chats = self.sconn.Chats
        for i in range(0,len(self.chats)):
            if(self.chats[i].FriendlyName.find(chatname) != -1):
                print(str(i) + " " + self.chats[i].FriendlyName)
                roomslike = roomslike + [i]
        return(roomslike)


    #Get index for a named chat
    def get_chatroom(self, chatname):
        
        #Find the named chat in the list of attached chats
        self.chats = self.sconn.Chats
        for i in range(0,len(self.chats)):
            if(self.chats[i].FriendlyName.find(chatname) != -1):
                print("Found chatroom " + self.chats[i].FriendlyName)
                return(i)
        return(-1)
        
    
    #Get messages for a chat
    def get_messages(self, roomid):
        
        #Grab the messages for this chat
        messages = self.chats[roomid].Messages
        print(self.chats[roomid].FriendlyName)

        #Convert and sort (by time) the list of messages
        self.mlist = list(messages)
        self.mlist.sort(message_timestamp_cmp)

        return(self.mlist)

    #Write messages for a chatroom to a csv file
    def dump_messages(self, chatroom):
        
        #Open CSV file to hold message data
        roomname = self.chats[chatroom].FriendlyName
        roomplain = re.sub('[\W_]+', '', roomname)
        outfile = "skypechat_" + roomplain[:min(len(roomplain),30)] + ".csv"
        f = open(outfile, 'wb')
        csvout = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        self.get_messages(chatroom)
        for m in self.mlist:
            row = []
            row += [m.FromHandle.encode('utf-8')]
            row += [m.Body.encode('utf-8')]
            row += [m.Timestamp]
            row += [m.Type]
            csvout.writerow(row)
        f.close()


    def get_members(self, chatroom):

        members = {}
        #Write member details to array
        for u in self.chats[chatroom].Members:
            skypeid = u.Handle.encode('utf-8')
            members[skypeid] = {}
            members[skypeid]['Handle']       = skypeid
            members[skypeid]['DisplayName']  = u.DisplayName.encode('utf-8')
            members[skypeid]['FullName']     = u.FullName.encode('utf-8')
            members[skypeid]['Aliases']      = u.Aliases #is a list
            members[skypeid]['About']        = u.About.encode('utf-8')
            members[skypeid]['MoodText']     = u.MoodText.encode('utf-8')
            members[skypeid]['RichMoodText'] = u.RichMoodText.encode('utf-8')
            members[skypeid]['Birthday']     = u.Birthday #is a DateTime
            members[skypeid]['Sex']          = u.Sex,
            members[skypeid]['Homepage']     = u.Homepage.encode('utf-8')
            members[skypeid]['PhoneHome']    = u.PhoneHome.encode('utf-8')
            members[skypeid]['Language']     = u.Language.encode('utf-8')
            members[skypeid]['LanguageCode'] = u.LanguageCode.encode('utf-8') 
            members[skypeid]['NumberOfAuthBuddies'] = u.NumberOfAuthBuddies
            members[skypeid]['LastOnline']   = u.LastOnline
            members[skypeid]['Country']      = u.Country.encode('utf-8')
            members[skypeid]['CountryCode']  = u.CountryCode.encode('utf-8')
            members[skypeid]['Province']     = u.Province.encode('utf-8')
            members[skypeid]['City']         = u.City.encode('utf-8')
            members[skypeid]['Timezone']     = u.Timezone
            members[skypeid]['BuddyStatus']  = u.BuddyStatus #Integer: 0 or 3

        return(members)

    
    #Write list of members to a csv file
    def dump_members(self, chatroom):

        members = self.getmembers(chatroom)
        
        #Open file to hold members list
        outfile = "skypemembers_" + roomplain[:min(len(roomplain),30)] + ".csv"
        f = open(outfile, 'wb')
        csvout = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        csvout.writerow(["Handle", "DisplayName", "FullName", #"Aliases",
                         "About", "MoodText", "RichMoodText", #"Birthday", 
                         "Sex", "Homepage", "PhoneHome", 
                         "Language", "LanguageCode", 
                         "NumbrOfAuthBuddies", "LastOnline",
                         "Country", "CountryCode", "Province", "City", 
                         "Timezone"])

        #Write members list to file
        for skypeid in members:
            row = []
            row += [members[skypeid]['Handle']]
            row += [members[skypeid]['DisplayName']]
            row += [members[skypeid]['FullName']]
            #row += [members[skypeid]['Aliases']]
            row += [members[skypeid]['About']]
            row += [members[skypeid]['MoodText']]
            row += [members[skypeid]['RichMoodText']]
            #row += [members[skypeid]['Birthday']]
            row += [members[skypeid]['Sex']]
            row += [members[skypeid]['Homepage']]
            row += [members[skypeid]['PhoneHome']]
            row += [members[skypeid]['Language']]
            row += [members[skypeid]['LanguageCode']]
            row += [members[skypeid]['NumberOfAuthBuddies']]
            row += [members[skypeid]['LastOnline']]
            row += [members[skypeid]['Country']]
            row += [members[skypeid]['CountryCode']]
            row += [members[skypeid]['Province']]
            row += [members[skypeid]['City']]
            row += [members[skypeid]['Timezone']]
            csvout.writerow(row)
            
        f.close()
        return()
        

