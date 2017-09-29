from itertools import izip

print "#x,y,z,u,v,w,a,b,c,d,e,f"
with open("initial_position.txt") as textfile1, open("displacement.txt") as textfile2: 
    for x, y in izip(textfile1, textfile2):
        x = x.strip()
        y = y.strip()
        print x + y + ",0.000,0.000,0.000,0.000,0.000,0.000"
