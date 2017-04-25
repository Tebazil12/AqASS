from vectors import Line, Point, Plane, get_direction
from locations import dist_between, Location
from gps import *
import numpy as np
from time import sleep
from datetime import datetime

class Behaviour():
    def __init__(self,perimiter_lines, perimiter_locs, obstacles, WEIGHT_WAYP,AT_WAYPOINT,ROUNDING, gpsp,ser):
        self.perim_lines = perimiter_lines
        self.perim_locs =perimiter_locs
        self.obstacles = obstacles
        self.WEIGHT_WAYP = WEIGHT_WAYP
        self.AT_WAYPOINT =AT_WAYPOINT
        self.ROUNDING =ROUNDING
        self.gpsp =gpsp
        self.ser = ser
        
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
        #return lanes

    def areascan(RESOLUTION):
        """
        The area scanning behaviour. Should take the perimiter points, perimiter
        lines and obstacles. Will then navigate within the perimiter along lanes.
        """
        print 'Starting area scan...'
        waypoints = []
        #waypoints= end_of_lanes(lanes)#TODO is it worth init these on  every line instead of all the start - prevent miss-match lines to waypoints
        #TODO find closest point on lane as first point, and put drift left/right as appropriate
        
        lanes = get_lanes(RESOLUTION)
        for lane in lanes: # TODO what happens when restart half way through
            while gpsd.fix.speed > 20 or (gpsd.fix.latitude == 0 and gpsd.fix.longitude == 0):  #decide better value for gps being silly and jumping
                pass #if after so long nothing happens, stop arduino/motors and wait/sleep?
            drift = Plane(0,WEIGHT_PLANE) #bearing along line, will need to define left of origin and right of origin, then alternate between them
            #prev_location = None # where the boat was located at last iteration
            #prev_speed = None
            prev_time = None ##TODO
            current_location = Location(gpsd.fix.latitude,gpsd.fix.longitude)
            # While the next waypoint hasn't been reached
            while dist_between(current_location, current_waypoint) >= AT_WAYPOINT:
                # Checking if stuck
            #    if (time_now-prev_time)% 4 == 0: #TODO time this value with corners etc
            #        if gpsd.fix.speed < 1 and prev_speed < 1:
            #            # Make new obstacle infront of boat
            #            obstacles.append(Point(current_location),WEIGHT_OBST)#TODO this should be infront of boat, not on boat!
            #        prev_location = current_location
                # add vectors
                overall = np.array([0,0])
                if len(obstacles) >=1:
                    for obs in obstacles:
                        overall += obs.get_vector
                if len(perimeter_lines) >= 1:
                    for bnd in perimeter_lines:
                        overall += bnd.get_vector
                overall += lane.get_vector
                overall += current_waypoint.get_vector
                overall += drift.get_vector
                ###
                direction = get_direction(overall)
                #TODO send direction to arduino
                
                current_location = Location(gpsd.fix.latitude,gpsd.fix.longitude) #TODO get stuff from gps
    ###TODO "if stuck" should be in seperate function to allow use in other behaviours
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


    def go_to_waypoint(self, target_loc, prev_loc=None):
        """
        The station keeping behaviour. Will take the boat to a specified point
        and stay at the specified point for a set length of time (station_time).
        """
        print 'Going to waypoint',target_loc,' ...'

        logfile = open("logs.csv","a")
        logfile.write("\rNEW_LOG Waypoint%s %s"%(target_loc,str(datetime.now())))
        logfile.close()

        target_pt = Point(target_loc, self.WEIGHT_WAYP)
        current_location = Location(self.gpsp.get_latitude(),self.gpsp.get_longitude())
        #print 'current location:', current_location
        
    #    prev_speed = None
        prev_time = None ##TODO
        

        # Check there is a gps fix
        while (current_location.lat_deg == 0 and current_location.lon_deg == 0 )\
              or current_location.lat_deg is NaN or current_location.lon_deg is NaN:
            print 'gps lost...' #TODO if after so long nothing happens, stop arduino/motors and wait/sleep?
            sleep(1)
            current_location = Location(self.gpsp.get_latitude(),self.gpsp.get_longitude())

        if prev_loc == None:
            prev_loc = current_location
        path = Line([prev_loc,target_loc],10) #TODO make this take WEIGHT_LANE rather than constant
            
        print 'Distance to target: ',dist_between(current_location, target_loc)
        while dist_between(current_location, target_loc) >= self.AT_WAYPOINT:# While the next waypoint hasn't been reached
           # print 'current location:', current_location
           # print 'target location:',target_loc
            
            # Checking if stuck
    #        if (time_now-prev_time)% 4 == 0: #TODO time this value with corners etc
    #            if gpsp.get_speed() < 1 and prev_speed < 1:
    #                # Make new obstacle infront of boat
    #                obstacles.append(Point(current_location),WEIGHT_OBST)#TODO this should be infront of boat, not on boat!
    #            prev_speed = gpsp.get_speed() #TODO this might change between comparsion and setting - use constant for comparison first!
                
            # Add vectors    
            overall = np.array([0,0])

            if len(self.obstacles) >=1:
                for obs in self.obstacles:
                    overall += obs.get_vector(current_location,self.ROUNDING)
                    
            if len(self.perim_lines) >= 1:       
                for bnd in self.perim_lines:
                    overall += bnd.get_vector(current_location,self.ROUNDING)
                
            overall += path.get_vector(current_location,self.ROUNDING)
            overall += target_pt.get_vector(current_location,self.ROUNDING)
            
            direction = int(get_direction(overall))
            
            #TODO send direction to arduino
            
            thing = 'h(' + str(direction) +')'
            print(thing)
            thing = thing.encode('utf-8')
            self.ser.write(thing)
            
            
            print '----Direction:', direction, '----'
            print 'Distance to target: ',dist_between(current_location, target_loc)
            print "\r%s,%s,\"%s\",W"%(current_location.lat_deg,current_location.lon_deg,direction)

            # Save data to log file
            logfile = open("logs.csv","a")
            logfile.write("\r%s,%s,\"%s Bearing: %s Dist: %s\",W"%(current_location.lat_deg,current_location.lon_deg,str(datetime.now().strftime('%H:%M:%S')),direction,dist_between(current_location, target_loc)))
            logfile.close()
            
            sleep(1)

            # Refresh values for comparison on next iteration of loop
            current_location = Location(self.gpsp.get_latitude(),self.gpsp.get_longitude()) #TODO get stuff from gps
            # Check the gps has a fix and hasn't jumped
            while self.gpsp.get_speed() > 20 or (current_location.lat_deg == 0 and current_location.lon_deg == 0 ) \
                  or current_location.lat_deg is NaN or current_location.lon_deg is NaN:  
                print 'gps lost...' #TODO if after so long nothing happens, stop arduino/motors and wait/sleep?
                sleep(1)
                current_location = Location(self.gpsp.get_latitude(),self.gpsp.get_longitude())
                
        print 'Finished station keeping...'

    def simple_areascann(self, waypoints):
        """
        This is a very simplistic areascanning behaviour. Given a list of waypoints
        within the boundaries of the lake, it will navigate to those points
        in the order specified (calling go_to_waypoint() for every waypoint
        in the list.
        """
        logfile = open("logs.csv","a")
        logfile.write("\rNEW_LOG SimpleScan %s"%(str(datetime.now())))
        logfile.close()
        
        for i, pnt in enumerate(waypoints):
            print '-------------------- going to',pnt, '--------------------\n'
            if i > 0:
                self.go_to_waypoint(pnt, waypoints[i-1])
            else:
                self.go_to_waypoint(pnt)
            
            

        print 'Finished Areascann...'
        
    
        
        
