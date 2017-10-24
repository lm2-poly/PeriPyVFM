import csv
import sys


with open(sys.argv[1], 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     spamreader.next()
     i = 0
     print "#id,x,y,z,u,v,w"
     for row in spamreader:
         x = float(row[0])
         y = float(row[1])
         print  str(i)+","+row[0]+","+row[1]+","+row[2]+","+str((-x/64.)*(y/32.))+","+str((48.*48.*48.*48.-x*x*x*x)/(48.**4./32.))+",0."
         i += 1
