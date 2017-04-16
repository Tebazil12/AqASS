class Vector(object):
    """
    Base class for all types of vector feild "objects". 
    """
    def __init__(self,location,weight):
        self.location = location # for point this will be one Location, for a line it will be two
        self.weight = weight
   
    def get_vector(self, loc_current):
        """
        Return the vectorized force experienced at the given location due 
        to the given object. Returns a 1D np.array in the form 
        ([xforce,yforce]).
        """
        dist = self.get_dist_to(loc_current)
        bearing = bearing_to(loc_current ,self.closest_point(loc_current))
        y_force = np.around(self.weight*(dist*np.degrees(np.cos(bearing)))**2,\
            ROUNDING)
        x_force = np.around(self.weight*(dist*np.degrees(np.cos(90-bearing)))\
            **2, ROUNDING)
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
    """
    Represents a point force which can either be attractive or repulsive.
    """
    def __str__(self):
        return "Point[%s,%s]"%(self.location, self.weight)
    
    def get_dist_to(self, loc2):
        return dist_between(self.location, loc2)
        
    def closest_point(self,loc2):
        return self.location

class Line(Vector):
    """
    Represents a line between two locations which is attractive or repulsive.
    """
    def closest_point(self, loc2):
        """
        Return the point on the line which is closest to loc2.
        """
        #location[0] location[1] loc2
        #print self.location[1].lat_deg
        #print type(self.location)
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
        print temp[0]
        lec = Location(self.location[0].lat_deg \
            + temp[0],self.location[0].lat_deg + temp[1])
        return lec
        
    def get_dist_to(self, loc2):
        return dist_between(self.location, self.closest_point(loc2))
        #return GPS_to_dist(self.location, loc2)

class Plane(Vector):
    """
    Represents a force of a set weight in a set direction at all locations.
    """
    
    def __init__(self,direction,weight):
        self.direction = direction # for point this will be one Location, for a line it will be two
        self.weight = weight
        self.vector = self.get_vector()
   
    def get_vector(self, loc_current=None):# extra makes more interchangeable 
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