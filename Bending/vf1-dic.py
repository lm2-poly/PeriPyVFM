# -*- coding: utf-8 -*-
# Script to generate the first virtual field for the displacement obtained by digital
# image correlation
#@author: rolland.delorme@polymtl.ca
#@author: patrick.diehl@polymtl.ca

import csv
import sys

S = 75.

with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+",0.,"+str(abs(float(row[0]))-S/2)+",0."
         i+=1
