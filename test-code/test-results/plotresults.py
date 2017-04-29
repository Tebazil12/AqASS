import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import csv
import re

#http://www.scipy-lectures.org/intro/matplotlib/auto_examples/plot_quiver_ex.html
#https://matplotlib.org/basemap/users/examples.html
#map = Basemap(projection='ortho',lat_0=54,lon_0=-3,resolution='l')
#map.drawcoastlines(linewidth=0.25)
#map.drawcountries(linewidth=0.25)
#map.fillcontinents(color='coral',lake_color='aqua')
# draw the edge of the map projection region (the projection limb)
#map.drawmapboundary(fill_color='aqua')

loc_file = open("big-feild-westward/logs-for-vis-vecs.csv", "rU") 
reader = csv.reader(loc_file)
list_1=[]
x = []
y = []
b = []
for i,row in enumerate(reader):
    #print row
    #print i
    if i%1 == 0:
        if len(row) > 0:
            that = row[2]
            print that
            if len(row[2]) >= 33: #this is really bodged together, warning will not work with bearing between 0 and 9
                here = that[:-5]
            else:
                here = that[:-4]
            t = re.sub("[^0123456789\.]","",here)
            
            print 'len', len(t)
            n = t[6:]
            m = n[:3]
            print 'm',m
            x.append(float(row[0]))
            y.append(float(row[1]))
            b.append(int(m))
        
        
    #list_1.append(Location(float(row[0]),float(row[1])))
loc_file.close()



#print x,y,b

y_b = np.cos(np.radians(b))
x_b = np.sin(np.radians(b))

#print y_b
#print x_b
#print "locs:"
#for i in perimeter:
#    print i    



#n = 8
#X, Y = np.mgrid[0:n, 0:n]
#T = np.arctan2(Y - n / 2., X - n/2.)
#R = 10 + np.sqrt((Y - n / 2.0) ** 2 + (X - n / 2.0) ** 2)
#U, V = R * np.cos(T), R * np.sin(T)

#plt.axes([0.025, 0.025, 0.95, 0.95])
#map.quiver(y, x, x_b, y_b,linewidths=0.1)#, R)#, alpha=.5)
plt.quiver(y, x, x_b, y_b,width=0.001,scale=1 / 0.015)#, R)#, alpha=.5)#http://matplotlib.org/examples/pylab_examples/quiver_demo.html
#plt.quiver(X, Y, U, V, edgecolor='k', facecolor='None', linewidth=.5)

#w_x =52.4003569,52.4008446,52.4008315,52.4003405,52.3996090
#w_y = -3.8704652,-3.8704813,-3.8697410,-3.8697892,-3.8690946





#plt.xlim(-1, n)
#plt.xticks(())
#plt.ylim(-1, n)
#plt.yticks(())
#map.scatter(w_y,w_x)
#plt.scatter(w_y,w_x)
plt.show()
