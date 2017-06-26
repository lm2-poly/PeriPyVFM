import csv
import numpy as np
from peripydic import *
import random
from scipy.optimize import minimize, fmin_cobyla
import sys

case = "sym"

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
 
def res1(vf1,vf2,vf3,vf4):
     Wext1=2.*(40*25)*(37/2)
     Wext2 = 0.
     Wext3 = 2.*(40*25)*np.sin(np.pi*37/(2*37))
     Wext4 = 0.
     vf1 += Wext1
     vf2 += Wext2
     vf3 += Wext3
     vf4 += Wext4
     return np.sqrt(vf1*vf1*0 + vf2*vf2*0 + vf3*vf3 + vf4*vf4) / np.sqrt(0*Wext1**2 + 0*Wext2**2 + Wext3**2 + Wext4**2)
 
def res2(vf1,vf2,vf3,vf4):
    return np.sqrt(vf1*vf1*0 + vf2*vf2 + vf3*vf3*0 + vf4*vf4)

def residual(P, deck):
    
    deck.bulk_modulus = P[0]
    deck.shear_modulus = P[1]
   
    problem = DIC_problem(deck)
    vf1 = 0.
    vf2 = 0.
    vf3 = 0.
    vf4 = 0.
    energy = 0.
    for i in range(0,len(u1)):
        #if deck.geometry.nodes[i][1] >= 7.:
        vf1 += np.dot(problem.force_int[i,:,1] , u1[i]) * deck.geometry.volumes[i] 
        vf2 += np.dot(problem.force_int[i,:,1] , u2[i]) * deck.geometry.volumes[i] 
        vf3 += np.dot(problem.force_int[i,:,1] , u3[i]) * deck.geometry.volumes[i] 
        vf4 += np.dot(problem.force_int[i,:,1] , u4[i]) * deck.geometry.volumes[i] 
        #energy += problem.strain_energy[i]
        #print problem.strain_energy[i]
    #print "Energies" ,vf1 , vf2 , energy
    
    
    if deck.vtk_writer.vtk_enabled == True:
        writeParaview(deck,problem)
    
    if case == "sym":
        print deck.bulk_modulus, deck.shear_modulus, res1(vf1,vf2,vf3,vf4)
        #sys.exit()
        return res1(vf1,vf2,vf3,vf4)
    else:
        print deck.bulk_modulus, deck.shear_modulus, res1(vf1,vf2)
        sys.exit()
        return res1(vf1,vf2)
    
    
    
    
bnds=((0.1,10000),(0.1,10000))   

if case == "sym":
    u1 = readVirtualField("./examples/mesh_vf1_sym.csv")
    u2 = readVirtualField("./examples/mesh_vf2_sym.csv")
    u3 = readVirtualField("./examples/mesh_vf3_sym.csv")
    u4 = readVirtualField("./examples/mesh_vf4_sym.csv")

    deck = DIC_deck("examples/input_elas_2D_sym.yaml")

else:
    u1 = readVirtualField("./examples/mesh_vf.csv")
    u2 = readVirtualField("./examples/mesh_vf.csv")

    deck = DIC_deck("examples/input_elas_2D.yaml")


#p = np.array((random.uniform(0.1, 10.) * 1000., random.uniform(0.1, 10.) * 1000.), dtype=float)
p = np.array([3333.3333,1538.4615])

#res = minimize(residual, p, args=(deck), method='COBYLA', tol=1e-8,
 #                  options={'rhobeg': 100.,'disp': True })
 
res = minimize(residual, p, args=(deck), method='L-BFGS-B', bounds=bnds)

print res.x
