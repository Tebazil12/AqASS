import threading
from gps import *

class GpsPoller(threading.Thread): 
    """
    Class to controll the GPS. Uses a new thread.
    
    The code for using gpsd was copied, and adapted, from  an example class 
    written by     Dan Mandle (http://dan.mandle.me), September 2012, which 
    can be found at 
    http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
    """
    def __init__(self):
        """
        Initialize the new thread and start watching gps.
        """
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true
 
    def run(self):
        while self.running:
            self.gpsd.next() #this will continue to loop and grab EACH
                                #set of gpsd info to clear the buffer

    def init(self):
        """
        Start the GPS and wait for GPS to get a fix before continuing.
        """
        self.start()
        while(self.gpsd.fix.latitude == 0 and self.gpsd.fix.longitude == 0)or\
                self.gpsd.fix.latitude is NaN or self.gpsd.fix.longitude is NaN:
                # If working near 0,0 change this!
            print "waiting for gps fix..."
            time.sleep(1)        
    
    def get_latitude(self):
        """ Return the GPS's current latitude. """
        return self.gpsd.fix.latitude

    def get_longitude(self):
        """ Return the GPS's current longitude. """
        return self.gpsd.fix.longitude

    def get_speed(self):
        """ Return the GPS's current speed. """
        return self.gpsd.fix.speed
    
 
