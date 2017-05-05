from locations import dist_between,bearing_to,location_at,wrap_degrees,Location
import numpy as np

class Vector(object):
    """
    Base class for all types of vector feild "objects". 
    """
    def __init__(self,location,weight):
        self.location = location # for point location will be one Location, 
                                               # for a line it will be two.
        self.weight = weight
   
    def get_vector(self, loc_current,ROUNDING):
        """
        Return the vectorized force experienced at the given location due 
        to the given object. Returns a 1D np.array in the form 
        ([xforce,yforce]).
        """
        dist = self.get_dist_to(loc_current)

        bearing = bearing_to(loc_current ,self.closest_point(loc_current))
        
        if self.weight >= 0: # This is attractive, so takes form f=mr**2
            force = self.weight*(dist**2)
            
            # Prevent the attractive force overpowering obstacles/boundaries
            force = constrain_force(force, -100, 100)
            
            # fy = fcos(bearing), fx = fsin(bearing)
            y_force = np.around(force*np.cos(np.radians(bearing)), ROUNDING)
            x_force = np.around(force*np.sin(np.radians(bearing)), ROUNDING)
            
            
        else: # This is repelling, so takes form f=m/r**2
            force = self.weight/(dist**2)

            # fy = fcos(bearing), fx = fsin(bearing)
            y_force = np.around(force*np.cos(np.radians(bearing)), ROUNDING)
            x_force = np.around(force*np.sin(np.radians(bearing)), ROUNDING)
            
        # these should be left as float for accuracy, later results to be 
        # converted to int for arduino to read
        self.vector = np.array([x_force,y_force])
        return self.vector

def constrain_force(force, limit_min, limit_max):
    """ Limit force to between limit_min and limit_max """
    if force > limit_max:
        return limit_max
    elif force < limit_min:
        return limit_min
    else:
        return force

def get_direction(vector):
    """
    Return the angle of the force experienced due to the given vector,
    as a heading between 0 and 359 degrees.
    """
    if vector[0]==0 and vector[1]==0: # as this might cause errors with atan 
        return 0 #TODO think of a better course of action to take here
    rad = np.arctan2(vector[0],vector[1])
    deg = wrap_degrees(np.degrees(rad))
    return deg

############################ POINT CLASS ######################################

class Point(Vector):
    """
    Represents a point force which can either be attractive or repulsive.
    """
    def __str__(self):
        return "Point[%s,%s]"%(self.location, self.weight)
    
    def get_dist_to(self, loc2):
        return dist_between(self.location, loc2)
        
    def closest_point(self,loc2):
        return self.location

############################ LINE CLASS #######################################

class Line(Vector):
    """
    Represents a line between two locations which is attractive or repulsive.
    """
    def closest_point(self, loc2):
        """
        Return the point on the line which is closest to loc2. 
        
        This was copied from assignment example solutions for Numerical Methods
        (*** ) assignment finding the shortest distace to a line, and adapted 
        for use here. 
        """
        u = np.array([self.location[1].lat_deg - self.location[0].lat_deg,\
            self.location[1].lon_deg - self.location[0].lon_deg])

        v = np.array([loc2.lat_deg-self.location[0].lat_deg,\
            loc2.lon_deg-self.location[0].lon_deg])

        c1 = u.dot(v)

        if c1<0:
            return self.location[0]

        c2 = u.dot(u)
        if c1>c2:
            return self.location[1]

        temp = (c1/c2)*u
        
        lec = Location(self.location[0].lat_deg \
            + temp[0],self.location[0].lat_deg + temp[1])

        return lec
        
    def get_dist_to(self, loc2):
        return dist_between(loc2, self.closest_point(loc2))

    def __str__(self):
        return "Line[%s,%s,%s]"%(self.location[0],self.location[1], self.weight)

################################ PLANE CLASS ##################################

class Plane(Vector):
    """
    Represents a force of a set weight in a set direction at all locations.
    """
    
    def __init__(self,direction,weight):
        self.direction = direction 
        self.weight = weight
        self.vector = self.get_vector()
   
    def get_vector(self, loc_current=None):# overrides default method 
        """
        Return the vectorized force experienced at the given location due 
        to the given object. Returns a 1D np.array in the form 
        ([xforce,yforce]).
        """
        y_force = np.around(self.weight*(np.cos(np.radians(self.direction)))\
            ,ROUNDING)
        x_force = np.around(self.weight*(np.cos(np.radians(90-self.direction)))\
            ,ROUNDING) 
        # these should be left as float for accuracy, later results to be 
        # converted to int for arduino to read
        self.vector = np.array([x_force,y_force])
        return self.vector

    def __str__(self):
        return "Plane[%s,%s]"%(self.direction, self.weight)
