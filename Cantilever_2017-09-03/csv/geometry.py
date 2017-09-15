import numpy as np
import matplotlib.pyplot as plt
import sys

# Parameter

P =	-50.
L =	75.
c =	12.5
t =	1.
E =	4000.
nu =	0.3
I =	t*(2*c)**3/12
K =	E/(3*(1-2*nu))
G =	E/(2*(1+nu))

# Mesh

dx = float(sys.argv[1])
dy = dx
x = 0. + dx/2.
y = -12.5 + dy/2.


#Computations

nx = int(L / dx)
ny = int((2 * c) / dy)

print nx * dx , ny * dy

xInit = []
yInit = []
u = []
v = []
s11 = []
s22 = []
s12 = []
e11 = []
e22 = []
gamma = []
strain_energy = []

for i in range(0,nx):
	for j in range(0,ny):
		xInit.append(x + i * dx)
		yInit.append(y + j * dy)

f1 = open('cantilever_deformed_2.csv', 'w')
f2 = open('mesh_vf2_2.csv', 'w')
f3 = open('mesh_vf3_2.csv', 'w')
f4 = open('cantilever_dic_2.csv', 'w')
f1.write("x,y,z,u,v,w,X,Y,Z,Sigma_11,Sigma_22,Sigma_12,Epsilon_11,Epsilon_22,Gamma_12,Strain Energy CCM\n")
f2.write("#id,x,y,z,u,v,w\n")
f3.write("#id,x,y,z,u,v,w\n")
f4.write("#x,y,z,u,v,w,a,b,c,d,e,f\n")
		
X = []
Y = []	
for i in range(0,len(xInit)):	
	u.append((P*yInit[i]/(6*E*I))*(3*(L**2-xInit[i]**2)+(2+nu)*(yInit[i]**2-c**2)))
	v.append((P/(6*E*I))*(3*nu*xInit[i]*yInit[i]**2+xInit[i]**3-3*L**2*xInit[i]+2*L**3+c**2*(4+5*nu)*(L-xInit[i])))
	s11.append(-P*xInit[i]*yInit[i]/I)
	s22.append(0)
	s12.append(P*(yInit[i]**2-c**2)/(2*I))
	e11.append((1/E)*(s11[i]-nu*s22[i]))
	e22.append((1/E)*(s22[i]-nu*s11[i]))
	gamma.append(s12[i]/G)
	strain_energy.append(0.5*(s11[i]*e11[i]+s22[i]*e22[i]+s12[i]*gamma[i]))	
	X.append(xInit[i]+u[i])
	Y.append(yInit[i]+v[i])
	f1.write(str(xInit[i]) + "," + str(yInit[i]) + ",0," + str(u[i]) + "," + str(v[i])  + ",0," + str(X[i])  + "," + str(Y[i]) + ",0," + str(s11[i])  + "," + str(s22[i])  + "," + str(s12[i])  + "," + str(e11[i])  + "," + str(e22[i])  + "," + str(gamma[i])  + "," + str(strain_energy[i])+"\n") 
	f2.write(str(i) + "," + str(xInit[i]) + "," + str(yInit[i]) + ", 0 , 0 ," + str(xInit[i]-L) + ",0\n")
	f3.write(str(i) + "," + str(xInit[i]) + "," + str(yInit[i]) + ", 0 ," + str(-(xInit[i]-L)*yInit[i]) + "," + str(0.5*(xInit[i]-L)**2) + ",0\n")	
	f4.write(str(xInit[i]) + "," + str(yInit[i]) + ",0," + str(u[i]) + "," + str(v[i])  + ",0.000,0.000,0.000,0.000,0.000,0.000,0.000\n")
f1.close()
f2.close()
f3.close()
f4.close()
#plt.scatter(X,Y)
#plt.savefig("deformed.pdf")
