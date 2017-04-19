#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
# Original taken from http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
# Edited by Lizzie Stone 2017
 
#import os
from gps import *
#from time import *
import time
import threading
import numpy as np
 
gpsd = None #seting the global variable

#os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
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
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while(gpsd.fix.latitude == 0 and gpsd.fix.longitude == 0):
      print "waiting for fix..."
      time.sleep(1)
    while True:
      #It may take a second or two to get good data
      print np.around(gpsd.fix.latitude,7),', ',np.around(gpsd.fix.longitude,7), 'speed (m/s) ' , gpsd.fix.speed
      print type(gpsd.fix.latitude)
      print "track", gpsd.fix.track
      time.sleep(1) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
