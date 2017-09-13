import numpy as np
import matplotlib.pyplot as plt

# Parameter

P =	-50
E =	4000
nu =	0.3
I =	1302.08333333333
K =	3333.33333333333
G =	1538.46153846154
L =	75
c =	12.5
t =	1

# Mesh

x = 0
y = 0
dx = 1
dy = 1


#Computations

nx = int(L / dx)
ny = int(c / dy)

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
strain = []

for i in range(0,nx):
	for j in range(0,ny):
		xInit.append(x + i * dx)
		yInit.append(y + j * dy)

f1 = open('mesh.csv', 'w')
		
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
	strain.append(0.5*(s11[i]*e11[i]+s22[i]*e22[i]+s12[i]*gamma[i]))	
	X.append(xInit[i]+u[i])
	Y.append(yInit[i]+v[i])
	f1.write(str(xInit[i]) + "," + str(yInit[i]) + ",0," + str(u[i]) + "," + str(v[i])  + ",0," + str(X[i])  + "," + str(Y[i])  + "," + str(s11[i])  + "," + str(s22[i])  + "," + str(s12[i])  + "," + str(e11[i])  + "," + str(e22[i])  + "," + str(gamma[i])  + "," + str(strain[i])+"\n") 

f1.close()
plt.scatter(X,Y)
plt.savefig("deformed.pdf")


		

	

