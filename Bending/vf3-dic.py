# -*- coding: utf-8 -*-
# Script to generate the second virtual field for the displacement obtained by a finite
# element simulations
#@author: rolland.delorme@polymtl.ca
#@author: patrick.diehl@polymtl.ca
import csv
import sys

L = 127.
W = 31.
          
with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         x = float(row[0])
         y = float(row[1])
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+","+str((x*abs(x)*y)/(L*W))+",0.,0."
         i += 1 
