import csv
import sys

L = 128
W = 32
S2 = 48

with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+","+str(-W*(float(row[0])/L)*(float(row[1])/W))+","+str(W*(float(row[0])**4-S2**4)/S2**4)+",0."
         i+=1