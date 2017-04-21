import threading
from gps import *

class GpsPoller(threading.Thread): ## Example class written by Dan Mandle http://dan.mandle.me September 2012
    def __init__(self):
        threading.Thread.__init__(self)
        #global gpsd #bring it in scope
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true
 
    def run(self):
        #global gpsd
        while self.running:
            self.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

    def get_latitude(self):
        return self.gpsd.fix.latitude

    def get_longitude(self):
        return self.gpsd.fix.longitude

    def get_speed(self):
        return self.gpsd.fix.speed
    
 
