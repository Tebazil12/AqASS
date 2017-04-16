# Copyright (c) 2017 Lizzie Stone
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import matplotlib.pyplot as plt
import unittest
import csv
from vectors import *
from locations import *
    
def read_locations(file_1):
    """ Read in co-ordinates of water perimeter."""
    #print "read"
    loc_file = open(file_1, "r") 
    reader = csv.reader(loc_file)
    list_1=[]
    for row in reader:
        print row
        list_1.append(Location(float(row[0]),float(row[1])))
    loc_file.close()
    
    #print "locs:"
    #for i in perimeter:
    #    print i    
    return list_1
    
def read_obstacles(): #TODO make this take args and return things
    """ Read in co-ordinates and weights of known objects."""
    obs_file = open("obstacles.csv", "r") 
    reader2 = csv.reader(obs_file)
    for row in reader2:
        print row
        obstacles.append(Point(Location(float(row[0]),float(row[1])),int(row[2])))
    obs_file.close()
    
def get_lanes(resolution):
    # Find furthest apart locations on water perimeter.
    far_loc1 = None
    far_loc2 = None
    max_dist = None
    for i in perimeter:
        for j in perimeter:
            dist = dist_between(i, j)
          #  print dist
            if max_dist == None or dist > max_dist:
                max_dist = dist
                far_loc1 = i
                far_loc2 = j
    print far_loc1 , far_loc2 ,max_dist
    
    
WEIGHT_OBST = -1 # will use f=m/r**2
WEIGHT_WAYP = 1 #will use f=mr**2
WEIGHT_LANE = 1 # will use f=mr**2
WEIGHT_BOUNDRY = -5 # probably f=m/r**2
WEIGHT_PLANE = 1

ROUNDING = 6 # no. of decimal places vectors are rounded to

RESOLUTION = 3 #this will be the distance between adjacent paths of the boat
AT_WAYPOINT = 2 # how close to the waypoint counts as being on the waypoint
    
waypoints = []
perimeter =[]#probably should make Lines too
obstacles =[]
start_finish = []
lanes = []

#current_lane = None #use while loop instead
current_waypoint = None

perimeter = read_locations("water.csv")
start_finish = read_locations("home.csv")
read_obstacles()

lanes = get_lanes(resolution)
waypoints= end_of_lanes(lanes)# is it worth init these on  every line instead of all the start - prevent miss-match lines to waypoints
#TODO find closest point on lane as first point, and put drift left/right as appropriate
for lane in lanes:
    drift = Plane() #bearing along line, will need to define left of origin and right of origin, then alternate between them
    prev_location = None # where the boat was located at last iteration
    prev_time = ##TODO
    while dist_between(current_location, current_waypoint) >= AT_WAYPOINT:
        if (time_now-prev_time)% 4 == 0: #TODO time this value with corners etc
            if dist_between(current_location, prev_location) < 1:
                obstacles.append(Point(current_location),WEIGHT_OBST)#TODO this should be infront of boat, not on boat!
            prev_location = current_location
        # add vectors
        overall = np.array([0,0])
        for obs in obstacles:
            overall += obs.get_vector
        for bnd in boundaries:
            overall += bnd.get_vector
        overall += lane.get_vector
        overall += current_waypoint.get_vector
        overall += drift.get_vector
        ###
        direction = get_direction(overall)
        #TODO send direction to arduino
        
        current_location = #TODO get stuff from gps

#print "locs:"
#for i in perimeter:
#    print i  
#print "locs done"
#print "home:"
#for i in start_finish:
#    print i  
#print "home done"



#maths to figure out positioning of channels

#next_waypoint = waypoint[1]

#get_current_location()

#if(less than distance(converted to gps degrees?)):
#    remove waypoint
#else:
    # if boat has not been moving (when its meant to be)
    #if average of last 10 gps points is less than 5m:
 #   if speed is < 1
  #      was last speed meant to be <1?
   #     if not 
    #        obstacle =  to list of objects
            
print ('done')
