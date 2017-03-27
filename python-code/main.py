import numpy as np
import matplotlib.pyplot as plt
import unittest

class Vector:
    def __init__(self,location,weight):
        self.location = location
        self.weight = weight
   
    def get_vector(self):
        self.vector = None #TODO
        return self.vector


class Obstacle(Vector):
    def __init__(self,location,weight,size):
        pass

    def get_vector():
        self.vector = None #TODO
        return self.vector

class Location:
    def __init__(self,lat,lon):
        self.lat_deg = lat
        self.lon_deg = lon
        self.lat_rad = np.radians(lat)
        self.lon_rad = np.radians(lon)

class waypoint(Vector):
    pass

def dist_to_GPS(location, dist, direction):
    """ Return the Location at distance, dist, away from the given Location 
    in the given direction.
    
    Keyword arguments:
    location -- the Location
    dist -- the distace away from location
    direction -- the direction from location as a heading in degrees 
    """
    pass

def GPS_to_dist(loc1, loc2):
    """ Return the direct distance between two Locations. Distance will 
    be scalar (e.g. always positive).
    
    Keyword arguments:
    loc1 -- the first Location
    loc2 -- the second Location
    """
    a = np.sin((loc1.lat_rad-loc2.lat_rad)/2.0)**2 + (np.cos(loc1.lat_rad) \
        * np.cos(loc1.lat_rad) * np.sin((loc1.lon_rad - loc2.lon_rad)/2.0)**2)
    c = 2* np.arcsin(np.sqrt(a))
    m = 6371000 * c 
    return np.around(m,1)


waypoints = None

#TODO read file of area co-ordinates
#TODO way of inputing start and end points

resolution = 1 #this will be the distance between adjacent paths of the boat

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
            

        
