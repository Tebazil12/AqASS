import threading
from gps import *

class GpsPoller(threading.Thread): ## orginal Example class written by Dan Mandle http://dan.mandle.me September 2012 http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
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

    def init(self):
        self.start()
        while(self.gpsd.fix.latitude == 0 and self.gpsd.fix.longitude == 0)or self.gpsd.fix.latitude is NaN or self.gpsd.fix.longitude is NaN:# If working near 0,0 change this!
            print "waiting for gps fix..."
            time.sleep(1)        
    
    def get_latitude(self):
        return self.gpsd.fix.latitude

    def get_longitude(self):
        return self.gpsd.fix.longitude

    def get_speed(self):
        return self.gpsd.fix.speed
    
 
