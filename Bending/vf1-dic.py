import csv
import sys


with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+",0.,"+str(abs(float(row[0]))-48.)+",0."
         i+=1