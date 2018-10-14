# -*- coding: utf-8 -*-
# Peridynamic virtual field method for extraction of the material properties
# from displacement obtained by a finite element simualtion
# 
#@author: rolland.delorme@polymtl.ca
#@author: patrick.diehl@polymtl.ca

import csv
import numpy as np
from peripydic import *
import random
import sys

# Read the displacment of the virtual field
# @param filename File name of the virtual field's file
# @return The components (u,v) of the virtual field
def readVirtualField(filename):
    
    data = []
    with open(filename, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            next(csvreader, None)
            for row in csvreader:
                data.append(np.array(map(float, row)))
                
    u = np.zeros((len(data),2))
    
    
    for i in range(0,len(data)):
        u[i][0] = data[i][4] 
        u[i][1] = data[i][5] 
        
    return u

# Computes the residual out of the internal and external energies
# @param Wint_vf1 Energy obtained by the first virtual field
# @param Wint_vf2 Energy obtained by the second virtual field
def res1(Wint_vf1,Wint_vf2):
     F = 1000.
     S = 96.
     W = 32.
     Wext_vf1 = F*S/2.  
     Wext_vf2 = 0.
     return np.sqrt((Wint_vf1+Wext_vf1)**2 + (Wint_vf2+Wext_vf2)**2 ) / np.sqrt(Wext_vf1**2 + Wext_vf2**2)
 
# Computes the internal energies and the residual
# @param P Material properties provided by nomad
# @param deck The loaded configuration 
# @return The current residual
def residual(P, deck):
    
    deck.bulk_modulus = P[0]
    deck.shear_modulus = P[1]
   
    problem = DIC_problem(deck)
    Wintvf1 = 0.
    Wintvf2 = 0.
    for i in range(0,len(u1)):
        Wintvf1 += np.dot(problem.force_int[i,:,1] , u1[i]) * deck.geometry.volumes[i] 
        Wintvf2 += np.dot(problem.force_int[i,:,1] , u2[i]) * deck.geometry.volumes[i]
    return res1(Wintvf1,Wintvf2)
      
# Read the two virtual fields
u1 = readVirtualField("./Bending/mesh_vf1_0_25.csv")
u2 = readVirtualField("./Bending/mesh_vf2_0_25.csv")

# Read the configuration file
deck = DIC_deck("./input_elas_2D.yaml")

# Read the provided material properties from nomad
file = open(sys.argv[1],'r')
values = file.readline().replace("\n","")
values = values.split(' ')
p = np.array((float(values[0]),float(values[1])), dtype=float)

# Compute the current residual with the material properties from nomad
print residual(p,deck) 

