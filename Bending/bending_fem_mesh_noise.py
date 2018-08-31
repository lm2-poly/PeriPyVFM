# -*- coding: utf-8 -*-
# Script to generate the second virtual field for the displacement obtained by a finite
# element simulations
#@author: rolland.delorme@polymtl.ca
#@author: patrick.diehl@polymtl.ca
import csv
import sys
import numpy as np
import random

mu = 0.0 # mean
sigma = 0.00005 #standard deviation
          
with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#x,y,z,u,v,w,a,b,c,d,e,f"
     for row in spamreader:
         x = float(row[0])
         y = float(row[1])
         z = float(row[2])
         u = float(row[3])
         v = float(row[4])
         w = float(row[5])
         print  str(x)+","+str(y)+","+str(z)+","+str(u+np.random.normal(mu, sigma))+","+str(v+np.random.normal(mu, sigma))+","+str(w)+",0.,0.,0.,0.,0.,0."
         i += 1 
