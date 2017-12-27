import csv
import sys

L = 128
W = 32
S = 96
t = 12.7
          
with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         x = float(row[0])
         y = float(row[1])
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+","+str(-(t**3)*(x/L**2)*(y/W**2))+","+str((x**4-(S/2)**4)/((S/2)**4/W))+",0."
         i += 1 
