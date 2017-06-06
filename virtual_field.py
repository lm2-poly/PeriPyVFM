import csv
import numpy as np
from peripydic import *
import random
from scipy.optimize import minimize, fmin_cobyla
import sys

def readVirtualField(filename):
    
    data = []
    with open(filename, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            next(csvreader, None)
            for row in csvreader:
                data.append(np.array(map(float, row)))
                
    u1 = np.zeros((len(data),2))
    u2 = np.zeros((len(data),2))
    
    
    for i in range(0,len(data)):
        u1[i][0] = data[i][3] * 1000.
        u1[i][1] = data[i][4] * 1000.
        u2[i][0] = data[i][6] * 1000.
        u2[i][1] = data[i][7] * 1000.
        
    return u1 , u2

def nu(P):
    return (3. * P[0] - 2. * P[1]) / (2. * (3. * P[0] + P[1]))

def residual(P, deck):
    
    #deck.bulk_modulus = P[0]
    #deck.shear_modulus = P[1]
   
    problem = DIC_problem(deck)
    vf1 = 0
    vf2 = 0
    energy = 0
    for i in range(0,len(u1)):
        if deck.geometry.nodes[i][1] >= 7.:
            vf1 += np.dot(problem.force_int[i,:,1] , u1[i]) * deck.geometry.volumes[i]
            vf2 += np.dot(problem.force_int[i,:,1] , u2[i]) * deck.geometry.volumes[i]   
            energy += problem.strain_energy[i]
    print vf1 , vf2 , energy
    vf1 += 45000   
    
    res = np.sqrt(vf1*vf1 + vf2*vf2)
    print deck.bulk_modulus, deck.shear_modulus, nu(P) , res
    
    sys.exit()
    
    return abs(4756.84121379 - res)


u1, u2 = readVirtualField("./examples/2D_VFM_inverse_dx1_small.csv")

#print u2

deck = DIC_deck("examples/input_elas_2D_short.yaml")


p = np.array((random.uniform(0.1, 10.) * 1000.,
                  random.uniform(0.1, 10.) * 1000.), dtype=float)

res = minimize(residual, p, args=(deck), method='COBYLA', tol=1e-3,
                   options={'rhobeg': 100.,'disp': True })

print res.x
