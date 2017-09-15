import csv
import matplotlib.pyplot as plt
data = []

with open('result.dat', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     i = 0
     tmp = -1
     for row in spamreader:
	data.append(row) 

     next = 8
     act = 0	
     m = [3,4,5,6,7,8,9,10]
     error = []
     for i in range(0,len(data)-1,2):
     
     	if act < next:
     		error.append(float(data[i+1][0]))
     		act +=1
     	else:	
      		act = 0 
      		plt.plot(m,error,label="h="+data[i-2][0])
      		error = []
plt.grid()
plt.xlabel("m")
plt.ylabel("residual")
plt.legend(loc=2)      		
plt.savefig("error.pdf")
        
         