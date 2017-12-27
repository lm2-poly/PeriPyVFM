import csv
import numpy as np
from peripydic import *
import random
import sys

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
    
def res1(Wint_vf1,Wint_vf2,Wint_vf3):
     Wext_vf1 = 48000. 
     Wext_vf2 = 0.
     Wext_vf3 = 32000.
     return np.sqrt((Wint_vf1+Wext_vf1)**2 + (Wint_vf2+Wext_vf2)**2 + (Wint_vf3+Wext_vf3)**2 ) / np.sqrt(Wext_vf1**2 + Wext_vf2**2 + Wext_vf3**2)
 

def residual(P, deck):
    
    deck.bulk_modulus = P[0]
    deck.shear_modulus = P[1]
   
    problem = DIC_problem(deck)
    vf1 = 0.
    vf2 = 0.
    vf3 = 0.
    #writeParaview(deck,problem) 
    for i in range(0,len(u1)):
        vf1 += np.dot(problem.force_int[i,:,1] , u1[i]) * deck.geometry.volumes[i] 
        #vf2 += np.dot(problem.force_int[i,:,1] , u2[i]) * deck.geometry.volumes[i] 
        vf3 += np.dot(problem.force_int[i,:,1] , u3[i]) * deck.geometry.volumes[i]
    return res1(vf1,vf2,vf3)
    
    
    
bnds=((0.1,10000),(0.1,10000))   


u1 = readVirtualField("./Bending/mesh_vf1_0_25.csv")
#u2 = readVirtualField("./Bending/mesh_vf2_0_25.csv")
#u3 = readVirtualField("./Bending/mesh_vf3_0_25.csv")
u3 = readVirtualField("./Bending/mesh_vf4_0_25.csv")

deck = DIC_deck("./input_elas_2D.yaml")

file = open(sys.argv[1],'r')
values = file.readline().replace("\n","")
values = values.split(' ')
p = np.array((float(values[0]),float(values[1])), dtype=float)
print residual(p,deck) 

