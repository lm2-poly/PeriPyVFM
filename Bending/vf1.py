# -*- coding: utf-8 -*-
# Script to generate the first virtual field for the displacement obtained by a finite
# element simulations
#@author: rolland.delorme@polymtl.ca
#@author: patrickdiehl@lsu.edu

import csv
import sys

S = 96.

with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         x = float(row[0])
         y = float(row[1])
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+",0.,"+str(abs(x)-S/2)+",0."
         i+=1
