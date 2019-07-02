# -*- coding: utf-8 -*-
# Script to generate the second virtual field for the displacement obtained by a finite
# element simulations
#@author: rolland.delorme@polymtl.ca
#@author: patrickdiehl@lsu.edu
import csv
import sys
import numpy as np

L = 126.7
W = 30.99
S = 75.
C = 4.5
SigL = (L/2.)/C
SigW = (W/2.)/C
          
with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         x = float(row[0])
         y = float(row[1])
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+",0.,"+str(abs(x)-S/2)+",0."
         #print  str(i)+","+row[0]+","+row[1]+","+row[2]+","+str(((2./W)*x*np.exp(-0.5*((x)/SigL)**2.))*(L/2*np.exp(-0.5*((y-W/2.)/SigW)**2.)))+","+str((-y/2*np.exp(-0.5*(x/SigL)**2.)))+",0.,0."
         i += 1  
