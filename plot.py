import csv
import numpy as  np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def readFile(file):
	with open(file, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ')
		data = []
		for row in reader:
			data.append(row)
	return np.array(data,dtype=float)

def plot(error,k,g,nu,ax,file,color):

	ax.plot_wireframe(k,g,error,label=str(file))
	#color = base_line.get_color()
	#last = len(k)-1
	ax.scatter(k,g,error,c=color)

data = readFile("run.dat")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

error = data[:,2]
k = data[:,0]
g = data[:,1]

plot(error,k,g,error,ax,0,error)

ax.scatter([3333.333],[1538.4615],[0],marker="*")


ax.set_xlabel("$K$")
ax.set_ylabel("$G$")
ax.set_zlabel(r"$e$")
plt.legend()
plt.show()