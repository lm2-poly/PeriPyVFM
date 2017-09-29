import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('text', usetex = True)
matplotlib.rc('font', **{'family' : "sans-serif"})

data = []

with open('../result.dat', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     i = 0
     for row in spamreader:
     	if i % 2:
		data.append(float(row[0])) 
		print row
	i +=1

    
     m = [3,4,5,6,7,8,9,10]
     h = [5,0.5,0.25,0.2,0.1,0.05]
     
     i = 0
     for n in h:
     	begin = i * len(m)
     	end = (i+1) * len(m)
     	plt.plot(m,data[begin:end],label="$h="+str(n)+"$")
     	i +=1	 
     
plt.grid()
plt.xlabel(r"$m$")
plt.ylabel(r"residual")
plt.legend(loc=2)
#plt.title(r"No gaussian noise")      		
plt.savefig("error_0.pdf")
        
         
