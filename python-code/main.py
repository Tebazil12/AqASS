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
#import matplotlib.pyplot as plt
import unittest
import csv
import time
import threading
from gps import *
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
    
def get_lanes(RESOLUTION):
    # Find furthest apart locations on water perimeter.
    far_loc1 = None
    far_loc2 = None
    max_dist = None
    for i in perimeter_locs:
        for j in perimeter_locs:
            dist = dist_between(i, j)
          #  print dist
            if max_dist == None or dist > max_dist:
                max_dist = dist
                far_loc1 = i
                far_loc2 = j
    print far_loc1 , far_loc2 ,max_dist

class GpsPoller(threading.Thread): ## Example class written by Dan Mandle http://dan.mandle.me September 2012
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
    
#-----SET UP-----#
    
WEIGHT_OBST = -1 # will use f=m/r**2
WEIGHT_WAYP = 1 #will use f=mr**2
WEIGHT_LANE = 1 # will use f=mr**2
WEIGHT_BOUNDRY = -5 # probably f=m/r**2
WEIGHT_PLANE = 1

ROUNDING = 7 # no. of decimal places vectors are rounded to

RESOLUTION = 3 #this will be the distance between adjacent paths of the boat
AT_WAYPOINT = 2 # how close to the waypoint counts as being on the waypoint
    
waypoints = []
perimeter_locs = read_locations("water.csv")
perimeter_lines =[] # TODO CANNOT USE NORMAL LINES! IF STARTING OUTSIDE OUTLINE, WILL END UP GOING AWAY FROM START AND MAP
obstacles =[]
start_finish = read_locations("home.csv")
lanes = get_lanes(RESOLUTION)

#current_lane = None #TODO write to a file/similar to make recovery easier?
current_waypoint = None

read_obstacles()#TODO make this take args and return!

try: # To stop gps thread from living if program throws an error
    gpsp = GpsPoller()
    gpsp.start()
    while(gpsd.fix.latitude == 0 and gpsd.fix.longitude == 0):# If working near 0,0 change this!
        print "waiting for gps fix..."
        time.sleep(1)

    #waypoints= end_of_lanes(lanes)#TODO is it worth init these on  every line instead of all the start - prevent miss-match lines to waypoints
    #TODO find closest point on lane as first point, and put drift left/right as appropriate


    #-----MAIN LOOP-----#
    for lane in lanes: # TODO what happens when restart half way through
        while gpsd.fix.speed > 20 or (gpsd.fix.latitude == 0 and gpsd.fix.longitude == 0):  #decide better value for gps being silly and jumping
            pass #if after so long nothing happens, stop arduino/motors and wait/sleep?
        drift = Plane(0,WEIGHT_PLANE) #bearing along line, will need to define left of origin and right of origin, then alternate between them
        #prev_location = None # where the boat was located at last iteration
        prev_speed = None
        prev_time = None ##TODO
        current_location = Location(gpsd.fix.latitude,gpsd.fix.longitude)
        # While the next waypoint hasn't been reached
        while dist_between(current_location, current_waypoint) >= AT_WAYPOINT:
            # Checking if stuck
            if (time_now-prev_time)% 4 == 0: #TODO time this value with corners etc
                if gpsd.fix.speed < 1 and prev_speed < 1:
                    # Make new obstacle infront of boat
                    obstacles.append(Point(current_location),WEIGHT_OBST)#TODO this should be infront of boat, not on boat!
                prev_location = current_location
            # add vectors
            overall = np.array([0,0])
            for obs in obstacles:
                overall += obs.get_vector
            for bnd in perimeter_lines:
                overall += bnd.get_vector
            overall += lane.get_vector
            overall += current_waypoint.get_vector
            overall += drift.get_vector
            ###
            direction = get_direction(overall)
            #TODO send direction to arduino
            
            current_location = Location(gpsd.fix.latitude,gpsd.fix.longitude) #TODO get stuff from gps
    #-------------------#
    print "\nKilling gps Thread..." # Should go at very end
    gpsp.running = False
    gpsp.join()
    
except Exception as e:
    print e.__doc__
    print e.message
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
print "Done.\nExiting."
  



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
            
print ('All Done')
