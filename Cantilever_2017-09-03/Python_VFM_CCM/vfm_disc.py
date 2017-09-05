import numpy as np
np.set_printoptions(threshold=np.nan)
from numpy import linalg
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    th = np.arctan2(y, x)
    return(th, rho)

def imagesc(x,y,c):
    plt.imshow(c,extent=(x.min(),x.max(),y.min(),y.max()),interpolation='nearest', cmap=cm.plasma)
    plt.colorbar()
    plt.show()

E = 200000 #MPa=N/mm^2
nu = 0.29

P = 7000 #Applied load in Newton

InputQ11 = E/(1-(nu**2))
InputQ12 = nu*E/(1-nu**2)

# Dimesions of the disk
Rad = 50. #mm
t = 2. #mm

# 2D-DIC parameter
Step = 5.
mmPerPix = 2*Rad/2000 # mm / pixel ratio
SmallArea = (Step*mmPerPix)**2

start = -Rad-(Step*mmPerPix/2)
stepsize = Step*mmPerPix
end = Rad+(Step*mmPerPix/2)
x = np.arange(start,end,stepsize)
y = np.arange(end,start,-stepsize)

# x and y coordinates in mm
xMat = np.zeros((len(y),len(x)),dtype=float)
for i in range(0,len(y)):
    xMat[i,:] = x

yMat = np.zeros((len(y),len(x)),dtype=float)    
for i in range(0,len(x)):
    yMat[:,i] = y

#  Determining the polar coordinates from the Cartesian    
theta = np.zeros((len(y),len(x)))    
r = np.zeros((len(y),len(x)))

for j in range(0,len(x)):
    for i in range(0,len(y)):
        th, radius = cart2pol(x[j],y[i])
        theta[i,j] = th
        r[i,j] = radius
    
# Mask
r[r > Rad] = 0
r[r > 0] = 1
imagesc(xMat,yMat,r)

# Stresses in MPa
sigma1 = 1. * (-2.*P/(np.pi*t))*(np.divide(np.multiply((Rad-yMat),xMat**2),((xMat**2)+(Rad-yMat)**2)**2)+np.divide(np.multiply(Rad+yMat,xMat**2),(xMat**2+(Rad+yMat)**2)**2)-(1./(2.*Rad)))

sigma2 = (-2.*P/(np.pi*t))* (np.divide((Rad-yMat)**3,((xMat**2)+(Rad-yMat)**2)**2) +  np.divide((Rad+yMat)**3,((xMat**2)+(Rad+yMat)**2)**2) - (1./(2.*Rad)))

sigma6 = (2.*P/(np.pi*t)) * ( np.divide(np.multiply((Rad-yMat)**2,xMat),((xMat**2)+(Rad-yMat)**2)**2) - np.divide(np.multiply((Rad+yMat)**2,xMat),((xMat**2)+(Rad+yMat)**2)**2))

# % Strains
epsilon1 = ((InputQ11/((InputQ11**2)-(InputQ12**2)))*sigma1) - ((InputQ12/((InputQ11**2)-(InputQ12**2)))*sigma2)

epsilon2 = -(InputQ12/((InputQ11**2)-(InputQ12**2))*sigma1) + ((InputQ11/((InputQ11**2)-(InputQ12**2)))*sigma2)

epsilon6 = (2./((InputQ11)-(InputQ12)))*sigma6

# VFM
# For Virtual Field #1
# U1=k2*x
# U2=k2*(-R-y)
# For Virtual Field #2
# U1=k2*x
# U2=0

# "A" matrix
A = np.zeros((2,2))

A[0,0] = np.sum(np.multiply(epsilon2,r))
A[1,1] = np.sum(np.multiply(epsilon2,r))
A[0,1] = np.sum(np.multiply(epsilon1,r))
A[1,0] = np.sum(np.multiply(epsilon1,r))

# "B" matrix
B = np.zeros((2))

B[0] = (-2.*P*Rad)/(t*SmallArea)
B[1] = 0.

# Solving "Q" matrix
Q = np.linalg.solve(A,B)

InputQ = np.zeros((2))
InputQ[0] = InputQ11
InputQ[1] = InputQ12

print "Result should be: Q11 =", InputQ[0] 
print "Q11_vfm =", Q[0]
print "Result should be: Q12 =", InputQ[1] 
print "Q12_vfm =", Q[1]

E_vfm = Q[0] *(1.-(Q[1]/Q[0])**2)
E_error = (E_vfm-E) / E
print "Result should be: E =", E 
print "E_vfm =", E_vfm
print "E_error_rel = ", E_error * 100.,"%"

nu_vfm = Q[1] / Q[0]
nu_error = (nu_vfm-nu)/nu
print "Result should be: nu =", nu 
print "nu_vfm =", nu_vfm
print "nu_error_rel = ", nu_error * 100.,"%"


    