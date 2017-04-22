from vectors import Line, Point, Plane
from locations import dist_between, Location
from gps import *
import numpy as np

class Behaviour():
    def __init__(self,perimiter_lines, perimiter_locs, obstacles):
        self.perim_lines = perimiter_lines
        self.perim_locs =perimiter_locs
        self.obstacles = obstacles
        
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


    def stationkeep(self, target_loc, WEIGHT_WAYP,AT_WAYPOINT,ROUNDING, gpsp, station_time=5):
        """
        The station keeping behaviour. Will take the boat to a specified point
        and stay at the specified point for a set length of time (station_time).
        """
        print 'Starting station keeping...'
        print 'what?', type(gpsp)
        if type(gpsp) is int :
            print 'how?!'
            return 
        target_pt = Point(target_loc, WEIGHT_WAYP)
        
    #    prev_speed = None
        prev_time = None ##TODO
        current_location = Location(gpsp.get_latitude(),gpsp.get_longitude())
        print 'current location:', current_location
        print current_location.lat_deg
        print current_location.lat_deg is NaN
        
        while gpsp.get_speed() > 20 or (current_location.lat_deg == 0 and current_location.lon_deg == 0 ) or current_location.lat_deg is NaN or current_location.lon_deg is NaN:  #decide better value for gps being silly and jumping
                print 'gps lost...' #TODO if after so long nothing happens, stop arduino/motors and wait/sleep?
                current_location = Location(gpsp.get_latitude(),gpsp.get_longitude())
        
        print 'Distance to target: ',dist_between(current_location, target_loc)
        while dist_between(current_location, target_loc) >= AT_WAYPOINT:# While the next waypoint hasn't been reached
            print 'current location:', current_location
            
            
            # Checking if stuck
    #        if (time_now-prev_time)% 4 == 0: #TODO time this value with corners etc
    #            if gpsp.get_speed() < 1 and prev_speed < 1:
    #                # Make new obstacle infront of boat
    #                obstacles.append(Point(current_location),WEIGHT_OBST)#TODO this should be infront of boat, not on boat!
    #            prev_speed = gpsp.get_speed() #TODO this might change between comparsion and setting - use constant for comparison first!
                # add vectors
            overall = np.array([0,0])
            for obs in self.obstacles:
                overall += obs.get_vector(current_location,ROUNDING)
            for bnd in self.perim_lines:
                overall += bnd.get_vector(current_location,ROUNDING)
            overall += target_pt.get_vector(current_location,ROUNDING)
            
            direction = get_direction(overall)
            #TODO send direction to arduino
            print 'Direction:', direction
                
            current_location = Location(gpsp.get_latitude(),gpsp.get_longitude()) #TODO get stuff from gps
        print 'Finished station keeping...'
