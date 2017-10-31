import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('text', usetex = True)
matplotlib.rc('font', **{'family' : "sans-serif"})

m = []
e = []

with open('m_val.csv', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in spamreader:
	m.append(float(row[0]))
	e.append(float(row[1]))
     

plt.plot(m,e,marker="o")     
plt.grid()
plt.xlabel(r"$m$")
plt.ylabel(r"residual")
#plt.legend(loc=2)
#plt.title(r"No gaussian noise")      		
plt.savefig("convergence.pdf")
        
         
