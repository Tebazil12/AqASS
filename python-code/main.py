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
        self.location = location # for point this will be one Location, for a line it will be two
        self.weight = weight
   
    def get_vector(self, loc_current):
        """
        Return the vectorized force experienced at the given location due 
        to the given object. Returns a 1D np.array in the form 
        ([xforce,yforce]).
        """
        dist = get_dist_to(self, loc_current)
        bearing = bearing_to(loc_current ,closest_point(loc_current))
        y_force = self.weight*(dist*np.degrees(np.cos(bearing)))**2
        x_force = self.weight*(dist*np.degrees(np.cos(90-bearing)))**2
        # these should be left as float for accuracy, later results to be 
        # converted to int for arduino to read
        self.vector = np.array([x_force,y_force])
        return self.vector
        
    def get_direction(self):#TODO check syntax
        """
        Return the angle of the force experienced due to the given vector,
        as a heading between 0 and 359 degrees.
        """
        vec = get_vector()        
        if vector[0]==0 and vector[1]==0: # as this might cause errors with atan TODO check
            return 0 #TODO think of a better course of action to take here! maybe take previous heading?(or not)
        rad = np.arctan2(vector[0],vector[1])
        deg = wrap_degrees(np.degrees(rad))
        return deg

class Point(Vector):
    def get_dist_to(self, loc2):
        return dist_between(self.location, loc2)
    def closest_point(self,loc2):
        return self.location

class Line(Vector):
    def get_dist_to(self, loc2):
        return dist_between(self.location, closest_point(loc2))
        #return GPS_to_dist(self.location, loc2)
    def closest_point(self, loc2):
        """
        Return the point on the line which is closest to loc2.
        """
        location[0] location[1] loc2
        u = np.array([location[1].lat-location[0].lat,location[1].lon-location[0].lon])
        v = np.array([loc2.lat-location[0].lat,loc2.lon-location[0].lon])
        c1 = u.dot(v)
        if c1<0:
            return location[0]
        c2 = u.dot(u)
        if c1>c2:
            return location[1]
        temp = (c1/c2)*u
        lec = Location(location[0].lat + temp[0],location[0].lat + temp[1])
        return lec

        
   
class Location:
    """ Holds the gps co-ordinates of a location """
    def __init__(self,lat,lon):
        self.lat_deg = lat
        self.lon_deg = lon
        self.lat_rad = np.radians(lat)
        self.lon_rad = np.radians(lon)



def location_at(location, dist, direction):
    """ 
    Return the Location at distance, dist, away from the given Location 
    in the given direction.
    
    Keyword arguments:
    location -- the Location
    dist -- the distace away from location
    direction -- the direction from location as a heading in degrees 
    """
    pass

def dist_between(loc1, loc2):
    """ 
    Return the direct distance between two Locations. Distance will 
    be scalar (e.g. always positive). Use haversine formula.
    
    Keyword arguments:
    loc1 -- the first Location
    loc2 -- the second Location
    """
    a = np.sin((loc1.lat_rad-loc2.lat_rad)/2.0)**2 + (np.cos(loc1.lat_rad) \
        * np.cos(loc1.lat_rad) * np.sin((loc1.lon_rad - loc2.lon_rad)/2.0)**2)
    c = 2* np.arcsin(np.sqrt(a))
    m = 6371000 * c 
    return np.around(m,1)

def bearing_to(loc1, loc2):
    """
    Return bearing, in degrees, of loc2 from loc1 (angle from line between 
    loc1-north clockwise to loc1-loc2), e.g.:
    
     N      loc2
      \      /
       \    /
        \__/
         \/ <- angle will be <90
        loc1

    loc2      N
      \      /
       \    /
        \  /
        /\/\ <- angle will be >270
        \__/
        loc1
    
    Use formulas from http://www.movable-type.co.uk/scripts/latlong.html
    """
    a = np.sin(loc2.lon-loc1.lon) * np.cos(loc2.lat)
    b = np.cos(loc1.lat)*np.sin(loc2.lat) - np.sin(loc1.lat)*np.cos(loc2.lat)\
        *np.cos(loc2.lon-loc1.lon)
    rad = np.arctan2(a,b) 
    return np.degrees(rad)
    
WEIGHT_OBST = -5
WEIGHT_WAYP = 5
WEIGHT_TRACK = 5
WEIGHT_BOUNDRY = -5
    
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
