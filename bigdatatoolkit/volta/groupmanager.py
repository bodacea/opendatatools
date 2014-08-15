#!/usr/bin/env python
# -*- coding: cp1252 -*-

'''
General manager for lists of people, groups and chats from Ning, Skype and
Googlegroups

#Example use:
from groupmanager import *
compare_skypening(skypecsv, ningexcel)

Sara-Jayne Farmer
2012
'''

import csv
import re
import xlrd

#======================================================================================
#Compare people lists from Skype and Ning
#
#Sara-Jayne Farmer
#2012
#======================================================================================
#def compare_skypening(skypecsv, ningexcel):
skypefile = "../../Data/skypechats/Skypepeople_SBTFgeneralchat_2012-12-23.csv"
ningfile  = "../../Data/ning_sbtf/sbtfning_download_members_2012-12-20.xls"

#Import ning list
ningskypeids = []
ningids = {}
ningnames = {}
wbk = xlrd.open_workbook(ningfile)
sh = wbk.sheet_by_name("memberdata")
for i in range(1,sh.nrows):
    ningaddress = sh.cell_value(i,1)
    ningid = ningaddress[45:]  #FIXIT: Bad hack, need to replace with search for u_
    ningskypeid = (sh.cell_value(i,16))
    if type(ningskypeid) == str or type(ningskypeid) == unicode:
        ningskypeid = ningskypeid.lower() #Work in lowercase for now
    realname = sh.cell_value(i,0)
    ningskypeids += [ningskypeid]
    ningids[ningskypeid] = ningid
    ningnames[ningid] = realname
##sh = wbk.sheet_by_name("MemberSummary") #For processed Ning excel files only
##for i in range(1,sh.nrows):
##    ningid = sh.cell_value(i,4)
##    ningskypeid = sh.cell_value(i,18)
##    realname = sh.cell_value(i,18)
##    ningskypeids += [ningskypeid]
##    ningids[ningskypeid] = ningid
##    ningnames[ningid] = realname

#Import skype list
skypeids = []
skypenames = {}
fskype = open(skypefile, 'rb')
csvin = csv.reader(fskype)
headers = csvin.next()
for row in csvin:
    skypeid = row[0]
    if type(skypeid) == str or type(skypeid) == unicode:
        skypeid = skypeid.lower() #Work in lowercase - it's easier
    fullname = row[2]
    skypeids += [skypeid]
    skypenames[skypeid] = fullname
fskype.close()

#Cross-check lists
sset = set(skypeids)
nset = set(ningskypeids)
snotn = sset.difference(nset)
nnots = nset.difference(sset)

#Basic paranoia about sock puppets
if len(sset) != len(skypeids):
    print("Duplicates in Skype's Skype ids")
if len(nset) != len(ningskypeids):
    print("Duplicates in Ning's Skype ids")

#Dump to file
fout = open("skypening.csv", 'wb')
csvout = csv.writer(fout)
csvout.writerow(['Skypeid', 'Ningid', 'Skype name'])
for u in snotn:
    csvout.writerow([u, '', skypenames[u]])
fout.close()

#   return(stops)
