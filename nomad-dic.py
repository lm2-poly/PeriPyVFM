# -*- coding: utf-8 -*-
# Peridynamic virtual field method for extraction of the material properties
# from displacement obtained by a finite element simualtion
# 
#@author: rolland.delorme@polymtl.ca
#@author: patrickdiehl@lsu.edu

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

def writeParaview(deck,problem):
    #ccm_class = IO.ccm.CCM_calcul(deck,problem)
    deck.vtk_writer.write_data(deck,problem,None)
    
def res1(Wint_vf1,Wint_vf2,Wint_vf3,Wint_vf4):
     # Force F to update
     F = 2500.
     S = 75.
     W = 30.99
     Wext_vf1 = (F*S/2) #   F*S/2.  
     Wext_vf2 = 0. #(-F*W/2)
     Wext_vf3 = 0.
     Wext_vf4 = 0.
     #print Wint_vf1 , Wint_vf2 , Wint_vf3 , Wint_vf4
     return np.sqrt((Wint_vf1+Wext_vf1)**2 + (Wint_vf2+Wext_vf2)**2 + (Wint_vf3+Wext_vf3)**2 + (Wint_vf4+Wext_vf4)**2) / np.sqrt(Wext_vf1**2 + Wext_vf2**2 + Wext_vf3**2 + Wext_vf4**2)
 

def residual(P, deck):
    
    deck.bulk_modulus = P[0]
    deck.shear_modulus = P[1]
   
    problem = DIC_problem(deck)
    Wintvf1 = 0.
    Wintvf2 = 0.
    Wintvf3 = 0.
    Wintvf4 = 0.
    writeParaview(deck,problem) 
    for i in range(0,len(u1)):
        Wintvf1 += np.dot(problem.force_int[i,:,1] , u1[i]) * deck.geometry.volumes[i] 
        Wintvf2 += np.dot(problem.force_int[i,:,1] , u2[i]) * deck.geometry.volumes[i] 
        #Wintvf3 += np.dot(problem.force_int[i,:,1] , u3[i]) * deck.geometry.volumes[i]
        #Wintvf4 += np.dot(problem.force_int[i,:,1] , u4[i]) * deck.geometry.volumes[i]
    return res1(Wintvf1,Wintvf2,Wintvf3,Wintvf4)
    
    
    
bnds=((500.,5000.),(500.,5000.))   


u1 = readVirtualField("./Bending/mesh_vf1_dic.csv")
u2 = readVirtualField("./Bending/mesh_vf2_dic.csv")
#u3 = readVirtualField("./Bending/mesh_vf3_dic.csv")
#u4 = readVirtualField("./Bending/mesh_vf4_0_25.csv")

deck = DIC_deck("./input_elas_2D-dic.yaml")

file = open(sys.argv[1],'r')
values = file.readline().replace("\n","")
values = values.split(' ')
p = np.array((float(values[0]),float(values[1])), dtype=float)
print residual(p,deck) 

