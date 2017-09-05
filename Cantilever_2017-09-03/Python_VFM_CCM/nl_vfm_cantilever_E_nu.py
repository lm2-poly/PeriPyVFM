import numpy as np
#np.set_printoptions(threshold=np.nan)
import random
from numpy import linalg
from scipy.optimize import minimize, fmin_cobyla


# Applied load (N)
P = -50.

# Nominal Elastic Parameters
E = 4000. # Young modulus MPa=N/mm^2
nu = 0.3 # Poisson ratio
G = E/(2*(1+nu))

# Dimensions
L = 75. # Length mm
l = 25. # Width
#L = 5. # Length mm
#l = 3. # Width
c = l/2
t = 1. # Thickness
I = t * l**3 / 12 # Second moment of area respect to z-axis mm^4

# CCD and 2D-DIC parameters
Step = 20. # in pixels => change this value to change the mesh size
mmPerPix = 0.05 # mm / pixel ratio
mesh_size = Step*mmPerPix
print "Mesh size is", mesh_size, "mm"
SmallArea = (mesh_size)**2 # in mm^2

x = np.arange(mesh_size/2,L,mesh_size)
y = np.arange(c-mesh_size/2,-c,-mesh_size)

# Initial positions
x_Mat = np.zeros((len(y),len(x)),dtype=float)
for i in range(0,len(y)):
    x_Mat[i,:] = x

y_Mat = np.zeros((len(y),len(x)),dtype=float)    
for i in range(0,len(x)):
    y_Mat[:,i] = y

# Actual displacement fields
#u_Mat = (P/(6*E*I)) * np.multiply(y_Mat , 3*(L**2 - x_Mat**2) + (2+nu)*(y_Mat**2 - c**2))
#v_Mat = (P/(6*E*I)) * ( 3*nu*np.multiply(x_Mat , y_Mat**2) + (x_Mat**3) - (3*L**2 * x_Mat) + (2 * L**3) + (c**2 * (4+5*nu) * (L-x_Mat)) )

# Actual positions
#X_Mat = x_Mat+ u_Mat
#Y_Mat = y_Mat+ v_Mat

# Actual stresses in MPa - sigma1:=sigma11 - sigma2:=sigma22 - sigma6:=sigma12
#sigma1 = (-P/I) * np.multiply(x_Mat,y_Mat)
#sigma2 = np.zeros((len(y),len(x)),dtype=float)
#sigma6 = (P/(2*I)) * (y_Mat**2 - c**2)

# Actual strains in MPa - epsilon1:=epsilon11 - epsilon2:=epsilon22 - epsilon6:=gamma12:=2*epsilon12
epsilon1 = (-P/(E*I)) * np.multiply(x_Mat,y_Mat)
epsilon2 = ((nu*P)/(E*I)) * np.multiply(x_Mat,y_Mat)
epsilon6 = (P/(2*I*G)) * (y_Mat**2 - c**2)

# Actual strains in MPa - epsilon1:=epsilon11 - epsilon2:=epsilon22 - epsilon6:=gamma12:=2*epsilon12
#epsilon1 = (1/E) * (sigma1 - nu*sigma2)
#epsilon2 = (1/E) * (sigma2 - nu*sigma1)
#epsilon6 = sigma6 / G

# Actual strain energy density (J/mm^3)
#w_dens = 0.5 * (np.multiply(sigma1,epsilon1) + np.multiply(sigma2,epsilon2) + np.multiply(sigma6,epsilon6))

def residual(input_prop):
    
    input_E = input_prop[0]
    input_nu = input_prop[1]
    Q11 = input_E / (1 - input_nu**2)
    Q12 = input_nu * Q11
    Q66 = (Q11 - Q12) / 2.
    
    # Actual stresses in MPa - sigma1:=sigma11 - sigma2:=sigma22 - sigma6:=sigma12    
    sigma1_tmp = Q11 * epsilon1 + Q12 * epsilon2
    sigma2_tmp = Q12 * epsilon1 + Q11 * epsilon2
    sigma6_tmp = Q66 * epsilon6

    ##### Virtual field #1
    # Linear Virtual Extension
    #u_Mat_vf1 = x_Mat - L
    #v_Mat_vf1 = np.zeros((len(y),len(x)),dtype=float)    
    
    # Virtual strains #1 in MPa
    #epsilon1_vf1 = np.ones((len(y),len(x)),dtype=float)
    #epsilon2_vf1 = np.zeros((len(y),len(x)),dtype=float)
    #epsilon6_vf1 = np.zeros((len(y),len(x)),dtype=float)
    
    # Internal virtual work #1 (J)
    #Wint_vf1 = - np.sum((np.multiply(sigma1_tmp,epsilon1_vf1) + np.multiply(sigma2_tmp,epsilon2_vf1) + np.multiply(sigma6_tmp,epsilon6_vf1)) * SmallArea)
    
    # External virtual work #1 (J)
    # Wext_vf1 = 0 because force and displacement are orthogonal
    #Wext_vf1 = P * 0.
    
    #####
    
    ##### Virtual field #2
    # Vertical Linear Virtual Displacement
    #u_Mat_vf2 = np.zeros((len(y),len(x)),dtype=float)  
    #v_Mat_vf2 = x_Mat - L  
    
    # Virtual strains #2 in MPa
    epsilon1_vf2 = np.zeros((len(y),len(x)),dtype=float)
    epsilon2_vf2 = np.zeros((len(y),len(x)),dtype=float)
    epsilon6_vf2 = np.ones((len(y),len(x)),dtype=float)
    
    # Internal virtual work #2 (J)
    Wint_vf2 = - np.sum((np.multiply(sigma1_tmp,epsilon1_vf2) + np.multiply(sigma2_tmp,epsilon2_vf2) + np.multiply(sigma6_tmp,epsilon6_vf2)) * SmallArea)
    
    # External virtual work #2 (J)
    # Wext_vf2 = P * (x - L)  with x = 0
    Wext_vf2 = P * (-L)
    
    #####
    
    ##### Virtual field #3
    # Parabolic Virtual Deflection
    #u_Mat_vf3 = - np.multiply((x_Mat-L),y_Mat) 
    #v_Mat_vf3 = 0.5 * (x_Mat - L)**2  
    
    # Virtual strains #3 in MPa
    epsilon1_vf3 = -y_Mat
    epsilon2_vf3 = np.zeros((len(y),len(x)),dtype=float)
    epsilon6_vf3 = np.zeros((len(y),len(x)),dtype=float)
    
    # Internal virtual work #3 (J)
    Wint_vf3 = - np.sum((np.multiply(sigma1_tmp,epsilon1_vf3) + np.multiply(sigma2_tmp,epsilon2_vf3) + np.multiply(sigma6_tmp,epsilon6_vf3)) * SmallArea)
    
    # External virtual work #3 (J)
    # Wext_vf3 = P * (x - L)**2 / 2  with  x = 0
    Wext_vf3 = P * 0.5 * (-L)**2
    
    #####

    ##### Virtual field #4
    # Sinusoidal Virtual Displacement
    #u_Mat_vf4 = np.multiply(y_Mat**3, np.sin(2. * np.pi * (x_Mat-L) / L)) 
    #v_Mat_vf4 = np.zeros((len(y),len(x)),dtype=float)
    
    # Virtual strains #4 in MPa
    #epsilon1_vf4 = (2. * np.pi / L) * np.multiply(y_Mat**3, np.cos(2. * np.pi * (x_Mat-L) / L))
    #epsilon2_vf4 = np.zeros((len(y),len(x)),dtype=float)
    #epsilon6_vf4 = 3.* np.multiply(y_Mat**2, np.sin(2. * np.pi * (x_Mat-L) / L))
    
    # Internal virtual work #4 (J)
    #Wint_vf4 = - np.sum((np.multiply(sigma1_tmp,epsilon1_vf4) + np.multiply(sigma2_tmp,epsilon2_vf4) + np.multiply(sigma6_tmp,epsilon6_vf4)) * SmallArea)
    
    # External virtual work #4 (J)
    # Wext_vf4 = 0 because force and displacement are orthogonal
    #Wext_vf4 = P * 0.
    
    #####
    
    #Residual function
    #res = np.sqrt(((Wint_vf1 + Wext_vf1)**2 + (Wint_vf2 + Wext_vf2)**2 + (Wint_vf3 + Wext_vf3)**2 + (Wint_vf4 + Wext_vf4)**2) / (Wext_vf1**2 + Wext_vf2**2 + Wext_vf3**2 + Wext_vf4**2))
    res = np.sqrt(((Wint_vf2 + Wext_vf2)**2 + (Wint_vf3 + Wext_vf3)**2) / (Wext_vf2**2 + Wext_vf3**2))
    
    #print "Wint_vf1 =", Wint_vf1
    #print "Wext_vf1 =", Wext_vf1
    #print "Wint_vf2 =", Wint_vf2
    #print "Wext_vf2 =", Wext_vf2
    #print "Wint_vf3 =", Wint_vf3
    #print "Wext_vf3 =", Wext_vf3
    #print "Wint_vf4 =", Wint_vf4
    #print "Wext_vf4 =", Wext_vf4
    
    #print "Residual =", res
    return res

input_prop = np.array((random.uniform(0.02, 20.) * 500., random.uniform(0., 2.) * 0.25), dtype=float)
#input_prop = np.array([1000000.,0.1])
#input_prop = np.array([E,nu])
#residual(input_prop)

output_prop = minimize(residual, input_prop, method='L-BFGS-B', bounds=((10.,10000.),(0.,0.5)))
print "E =", E
print "E_vfm =", output_prop.x[0]
print "Error_rel_E", (output_prop.x[0]-E)/E * 100., "%"
print "nu =", nu
print "nu_vfm =", output_prop.x[1]
print "Error_rel_nu", (output_prop.x[1]-nu)/nu * 100., "%"