import numpy as np
import sys
sys.path.insert(0, '../../python-code')
from main import *
#import unittest
import csv

#f = open('map.txt', 'w')
#print f

loc_file = open("water.csv", "r") 
reader = csv.reader(loc_file)
water =[]
for row in reader:
    print row
    water.append(Location(float(row[0]),float(row[1])))
loc_file.close()
print "locs:"
for i in water:
    print i
#print "sorted"
#blah = sorted(water)
#for i in blah:
#    print i
loc1 = None
loc2 = None
max_dist = None
for i in water:
    for j in water:
        dist = dist_between(i, j)
      #  print dist
        if max_dist == None or dist > max_dist:
            max_dist = dist
            loc1 = i
            loc2 = j
print loc1 , loc2 ,max_dist
#do more in main, not here!

print "now obsts"
obs_file = open("obstacles.csv", "r") 
reader2 = csv.reader(obs_file)
obstacles =[]
for row in reader2:
    print row
    obstacles.append(Point(Location(float(row[0]),float(row[1])),int(row[2])))
    
obs_file.close()
print "obs:"
loca = Location(52.426802,-4.091098)
for i in obstacles:
    print i.weight
   # print i.get_vector(loca) #TODO move this to own unit test!












