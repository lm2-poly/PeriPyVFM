import csv
import numpy as np
from peripydic import *
import random
from scipy.optimize import minimize, fmin_cobyla
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

def nu(P):
    return (3. * P[0] - 2. * P[1]) / (2. * (3. * P[0] + P[1]))

def writeParaview(deck,problem):
    #ccm_class = IO.ccm.CCM_calcul(deck,problem)
    deck.vtk_writer.write_data(deck,problem,None)
    
def res1(vf1,vf2):
     vf1 += 56000
     return np.sqrt(vf1*vf1 + vf2*vf2)
 
def res2(vf1,vf2):
    return np.sqrt(vf1*vf1 + vf2*vf2) / 56000.

def residual(P, deck):
    
    #deck.bulk_modulus = P[0]
    #deck.shear_modulus = P[1]
   
    problem = DIC_problem(deck)
    vf1 = 0
    vf2 = 0
    energy = 0
    for i in range(0,len(u1)):
        #if deck.geometry.nodes[i][1] >= 7.:
        vf1 += np.dot(problem.force_int[i,:,1] , u1[i]) * deck.geometry.volumes[i]
        vf2 += np.dot(problem.force_int[i,:,1] , u2[i]) * deck.geometry.volumes[i]   
        energy += problem.strain_energy[i]
    print "Energies" ,vf1 , vf2 , energy
    
    
    if deck.vtk_writer.vtk_enabled == True:
        writeParaview(deck,problem)
    
    print deck.bulk_modulus, deck.shear_modulus, res1(vf1,vf2) , res2(vf1,vf2)
    
    sys.exit()
    
    return res1(vf1,vf2)


u1 = readVirtualField("./examples/mesh_vf1.csv")
u2 = readVirtualField("./examples/mesh_vf2.csv")
#print u2

deck = DIC_deck("examples/input_elas_2D_short.yaml")


p = np.array((random.uniform(0.1, 10.) * 1000.,
                  random.uniform(0.1, 10.) * 1000.), dtype=float)

res = minimize(residual, p, args=(deck), method='COBYLA', tol=1e-3,
                   options={'rhobeg': 100.,'disp': True })

print res.x
