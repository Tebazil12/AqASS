import threading
import numpy as np
#from gps import *

class GpsPoller(threading.Thread): ## orginal Example class written by Dan Mandle http://dan.mandle.me September 2012 http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
    def __init__(self):
        #threading.Thread.__init__(self)
        #global gpsd #bring it in scope
        #self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true
        self.coords=[]
        self.currentcord=[]
        
    def run(self):
        #global gpsd
        #while self.running:
         #   self.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
        pass

    def init(self):
        for i in np.arange(52.3995452,52.4024385, 1):
            for j in np.arange(-3.8718760,-3.8677025,1):
                self.coords.append([np.around(i,7),np.around(j,7)])
        print 'coords done'
        #self.start()
        #while(self.gpsd.fix.latitude == 0 and self.gpsd.fix.longitude == 0)or\
        #        self.gpsd.fix.latitude is NaN or self.gpsd.fix.longitude is NaN:# If working near 0,0 change this!
        #    print "waiting for gps fix..."
        #    time.sleep(1)        
    
    def get_latitude(self):
        self.currentcord = self.coords.pop()
        print 'current coord',self.currentcord
        return self.currentcord[0]

    def get_longitude(self):
        return self.currentcord[1]

    def get_speed(self):
        return 4
    
 
