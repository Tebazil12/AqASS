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

############################ MODULES ##########################################

import numpy as np
#import matplotlib.pyplot as plt
import unittest
import csv
import time
import threading
import serial
from gps import *
from vectors import Line, Point, Plane
from locations import *
from behaviours import Behaviour
from gps_driver import GpsPoller

############################ FUNCTIONS ########################################
    
def read_locations(file_1):
    """ Read in co-ordinates of water perimeter."""
    #print "read"
    loc_file = open(file_1, "r") 
    reader = csv.reader(loc_file)
    list_1=[]
    for row in reader:
        #print row
        list_1.append(Location(float(row[0]),float(row[1])))
    loc_file.close()
    
    #print "locs:"
    #for i in perimeter:
    #    print i    
    return list_1
    
def read_obstacles(): #TODO make this take args and return things
    """ Read in co-ordinates and weights of known objects."""
    obs_file = open("course/obstacles.csv", "r") 
    reader2 = csv.reader(obs_file)
    for row in reader2:
        #print row
        obstacles.append(Point(Location(float(row[0]),float(row[1])),\
                                        int(row[2])))
    obs_file.close()

def get_perim_lines(perimeter_locs):
    """ Read in co-ordinates of perimeter."""
    # TODO SHOULD NOT USE NORMAL LINES! IF STARTING OUTSIDE OUTLINE, 
    # WILL END UP GOING AWAY FROM START AND MAP
    lines = []
    size = len(perimeter_locs)
    #print size
    for i, thing in enumerate(perimeter_locs):
        if i+1 == size:
            #print perimeter_locs[i], 'to', perimeter_locs[0]
            lines.append(Line([perimeter_locs[i],perimeter_locs[0]],\
                         WEIGHT_BOUNDRY))
        else:
            #print perimeter_locs[i], 'to', perimeter_locs[i+1]
            lines.append(Line([perimeter_locs[i],perimeter_locs[i+1]],\
                         WEIGHT_BOUNDRY))
    return lines
        
    
############################## SET UP #########################################
    
WEIGHT_OBST = 0     # -1 # will use f=m/r**2
WEIGHT_WAYP = 10    # will use f=mr**2
WEIGHT_LANE = 10    # will use f=mr**2
WEIGHT_BOUNDRY = -5 # probably f=m/r**2
WEIGHT_PLANE = 0    # 1

ROUNDING = 7    # no. of decimal places vectors are rounded to

RESOLUTION = 3  # distance between adjacent lanes in area scan
AT_WAYPOINT = 4 # distance from the waypoint that means being at the waypoint
    

perimeter_locs = read_locations("course/water.csv")
perimeter_lines = get_perim_lines(perimeter_locs) 
obstacles =[]
read_obstacles()#TODO make this take args and return!
start_finish = read_locations("course/home.csv")

ser = serial.Serial('/dev/ttyUSB1')

gpsp = GpsPoller()

try: # To stop gps thread from living if program throws an error
    
    gpsp.init()

    ############################ MAIN CODE ####################################
    if len(start_finish) == 2:
        end_loc = start_finish[1]
    start_loc = start_finish[0] # TODO handle errors if file is empty

    print 'Running behaviours...'
    bh = Behaviour(perimeter_lines, perimeter_locs, obstacles, WEIGHT_WAYP,\
                    AT_WAYPOINT, ROUNDING, gpsp, ser)

    simple_waypts = read_locations("course/waypoints.csv")
    bh.simple_areascann(simple_waypts)
    
    print 'Behaviours finished.'
    ############################ SHUTDOWN CODE ################################

    print 'Shutting everything down...'
    ser.write(b'e')
    x = ser.readline().strip()
    print 'the arduino said: ',x
    # TODO ask arduino to sleep repeatedly, if it does not confirm after 5 or 
    # so attempts, exit anyway
    ser.close()
    
    
    print "\nKilling gps Thread..." # Should go at very end
    gpsp.running = False
    gpsp.join()
    
except Exception as e:
    print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e
    print e.__doc__
    print e.message
    print "\nKilling Thread..."
    gpsp.running = False #TODO move this to gps-driver
    gpsp.join() # wait for the thread to finish what it's doing

print "Done.\nExiting."
            
print ('Python Done')
