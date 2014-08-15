#Plot fuel wood scarcity from a 10-by-10 grid of values in a csv file

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

fin = open('FuelwoodScarcity-L10-2010-poly-v03-geo.csv', 'rb')
csvin = csv.reader(fin)
headers = csvin.next()
datarray = {}
datrow = []
rownum = -1
#
for row in csvin:
  rownum += 1
  #print(rownum)
  if (rownum != 0) and (rownum % 10 == 0):
    #print('break')
    datarray[rownum-1] = datrow
    datrow = []
  datrow.append(row[2])
  #
datarray[rownum-1] = datrow #Catch the last row of data!
fin.close()
#
#Now plot the darned thing!
af = pd.DataFrame(datarray)

