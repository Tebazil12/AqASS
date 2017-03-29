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
import matplotlib.pyplot as plt
import unittest

def wrap_degrees(angle):
    while angle<0:
        angle += 360
    angle = angle % 360
    return angle

class Vector(object):
    def __init__(self,location,weight):
        self.location = location
        self.weight = weight

    def get_dist_to(self, location):
        pass
   
    def get_vector(self):
        """
        Return the vectorized force experienced at the given location due 
        to the given object. Returns a 1D np.array in the form 
        ([xforce,yforce]).
        """
        self.vector = None #TODO
        return self.vector
        
    def get_force(self, vector):#TODO check syntax
        """
        Return the force experienced due to the given vector. Returns a 1D
        np.array in the form ([magnitude,direction]), where direction is 
        a heading between 0 and 359 degrees.
        """        
        mag = sqrt(vector[0]**2 +vector[1]**2)
        direc = wrap_degrees(np.degrees(np.arctan2(vector[0],vector[1])))
        result = np.array([np.clip(mag,0,180),direc])
        return result

class Point(Vector):
    def get_dist_to(self, loc2):
        return GPS_to_dist(self.location, loc2)
    
    def get_vector():
        return 
    

#class Obstacle(Vector):
#    pass
        
class Line():
    pass

class Location:
    def __init__(self,lat,lon):
        self.lat_deg = lat
        self.lon_deg = lon
        self.lat_rad = np.radians(lat)
        self.lon_rad = np.radians(lon)



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
            
print ('done')
