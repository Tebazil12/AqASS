f = open("gps-plotting.csv","a")
n = 52.413506
r = -4.089003
a = 56
f.write("\r%s,%s,\"%s\",W"%(n,r,a) )
f.close()
