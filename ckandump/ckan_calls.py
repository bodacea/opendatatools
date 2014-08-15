#!/usr/bin/env python
''' 
Add and access data in CKAN2.0 instance (e.g. datahub.io)
References include:
* http://docs.ckan.org/en/ckan-2.0/api.html
* http://ckan.readthedocs.org/en/ckan-1.7.1/using-data-api.html

Sara-Jayne Terp, 2013
'''

import urllib2
import urllib
import json
import pickle
import ckanclient
import pprint

'''
call_ckan_api: 
Sara-Jayne Terp, 2013
'''

#Globals
ckan = None

def call_ckan_api(ckanurl, apikey, apicall, data):
  
  # Make the HTTP request.
  data_string = urllib.quote(json.dumps(data))
  headers = {'Authorization': apikey}
  req = urllib2.Request(ckanurl+'api/3/'+apicall, data_string, headers)
  response = urllib2.urlopen(req)
  
  # Use the json module to load CKAN's response into a dictionary.
  ## assert response.code == 200
  response_dict = json.loads(response.read())
  
  # Check the contents of the response.
  ## assert response_dict['success'] is True
  result = response_dict['result']
  ## pprint.pprint(result)
  return(result)

def check_ckan_package(ckanurl, apikey, packagename, ownername):
  action = "action/package_show"
  ckandata = {'name':packagename,'owner_org':ownername}
  result = call_ckan_api(ckanurl, apikey, action, ckandata)
  return(result)
  
def create_ckan_package(ckanurl, apikey, packagename, ownername):
  action = "action/package_create"
  ckandata = {'name':packagename,'owner_org':ownername}
  result = call_ckan_api(ckanurl, apikey, action, ckandata)
  return(result)

def create_ckan_resource(ckanurl, apikey, data, 
                         resourcename, packagename, ownername):
  action = "action/resource_create"
  #NB Must put owner_org in here, or call will fail
  ckandata = {'name':resourcename,
          'package_id':packagename,
          'owner_org':ownername}
  ckandata.update(data)
  result = call_ckan_api(ckanurl, apikey, action, ckandata)
  return(result)

#Read in CKAN and google keys
def read_keys(keyfile):
  fin = open(keyfile, 'rb')
  ckankeys = {}
  googlekeys = {}
  ckankeys['url'] = fin.readline().strip()
  ckankeys['apikey'] = fin.readline().strip()
  googlekeys['user'] = fin.readline().strip()
  googlekeys['pass'] = fin.readline().strip()
  googlekeys['doc'] = fin.readline().strip()
  fin.close()
  return(ckankeys, googlekeys)
  
def dump_ckan_to_pickle(keyfile):
  #Connect
  [ckankeys, googlekeys] = read_keys(keyfile)
  fout = open("pickled_ckan_contents.pk1", "wb")
  
  ckan = ckanclient.CkanClient(
    base_location=ckankeys['url']+'api',
    api_key=ckankeys['apikey'])
  
  #tag list
  tag_list = ckan.tag_register_get()
  pickle.dump(tag_list, fout, -1) #force pickle to use highest protocol available
  
  #packages
  package_entities = {}
  package_list = ckan.package_register_get()
  print package_list
  for package_name in package_list:
    ckan.package_entity_get(package_name)
    package_entities[package_name] = ckan.last_message
  pickle.dump(package_entities, fout, -1)
  
  #groups
  groups = {}
  group_list = ckan.group_register_get()
  print group_list
  for group_name in group_list:
    groups[group_name] = ckan.group_entity_get(group_name)
  pickle.dump(groups, fout, -1)
  
  ###datasets
  ##datasets = {}
  ##dataset_list = ckan.dataset_register_get()
  ##for dataset_name in dataset_list:
  ##  datasets[dataset_name] = ckan.dataset_entity_get(dataset_name)
  ##pickle.dump(datasets, fout, -1)
  
  fout.close()
  return()

def reverse_ckan_pickle(filename):
  
  fin = open(filename, 'rb')
  tags = pickle.load(fin)
  packages = pickle.load(fin)
  groups = pickle.load(fin)
  fin.close()
  return tags, packages, groups

  



