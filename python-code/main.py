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
from behaviours import Behaviour
    
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
    

perimeter_locs = read_locations("water.csv")
perimeter_lines =[] # TODO CANNOT USE NORMAL LINES! IF STARTING OUTSIDE OUTLINE, WILL END UP GOING AWAY FROM START AND MAP
obstacles =[]
read_obstacles()#TODO make this take args and return!
start_finish = read_locations("home.csv")


#current_lane = None #TODO write to a file/similar to make recovery easier?

try: # To stop gps thread from living if program throws an error
    gpsp = GpsPoller()
    gpsp.start()
    while(gpsd.fix.latitude == 0 and gpsd.fix.longitude == 0):# If working near 0,0 change this!
        print "waiting for gps fix..."
        time.sleep(1)

    #-----MAIN CODE-----#
    if len(start_finish) == 2:
        end_loc = start_finish[1]
    start_loc = start_finish[0] # TODO handle errors if file is empty, maybe use startup location

    bh = Behaviour(perimiter_lines, perimiter_locs, obstacles)
    bh.stationkeep(start_loc)
    bh.areascann(RESOLUTION)
    bh.stationkeep(end_loc, 1)
    #-------------------#
    
    #shuteverything down
    #tell arduino to sleeps
    # ask arduino to sleep so many times, if it doesnt after 5 or so, sleep pi anyway
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
  


            
print ('All Done')
