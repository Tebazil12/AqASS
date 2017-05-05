import numpy as np

def wrap_degrees(angle):
    """ Wrap the angle to be between 0 and 359. """
    while angle<0:
        angle += 360
    angle = angle % 360
    return angle
   
class Location:
    """ Hold the gps co-ordinates of a location, given in degrees. """
    def __init__(self,lat,lon):
        self.lat_deg = lat
        self.lon_deg = lon
        self.lat_rad = np.radians(lat)
        self.lon_rad = np.radians(lon)
        
    def __str__(self):
        return "[%s,%s]"%(self.lat_deg, self.lon_deg)


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
    a = np.sin(loc2.lon_rad-loc1.lon_rad) * np.cos(loc2.lat_rad)
    b = np.cos(loc1.lat_rad) * np.sin(loc2.lat_rad) - np.sin(loc1.lat_rad)\
        * np.cos(loc2.lat_rad) * np.cos(loc2.lon_rad-loc1.lon_rad)
    rad = np.arctan2(a,b) 
    return wrap_degrees(np.degrees(rad))
