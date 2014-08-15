'''
Pull basic decriptions (but not dataset data) from a CKAN node

Sara-Jayne Farmer
2013
'''

import ckanclient
import pickle

#Connect
fin = open("../key.txt", 'rb')
key = fin.read().strip()
fin.close()

fout = open("pickled_ckan_contents.pk1", "wb")

ckan = ckanclient.CkanClient(
  base_location='http://ec2-54-228-69-142.eu-west-1.compute.amazonaws.com/api',
  api_key=key)

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

def reverse_pickle(filename):

  fin = open(filename, 'rb')
  tags = pickle.load(fin)
  packages = pickle.load(fin)
  groups = pickle.load(fin)
  fin.close()
  return tags, packages, groups

