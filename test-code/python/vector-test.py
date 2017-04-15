import numpy as np
import sys
sys.path.insert(0, '../../python-code')
from main import *
import unittest

class TestVectors(unittest.TestCase):
    def test_Line(self):
        loc1 = Location(52.416801,-4.091099)
        loc2 = Location(52.415603,-4.090702)
        loc3 = Location(52.415602,-4.090701)
        loc4 = Location(52.416802,-4.091200)
        locs = [loc1,loc2]
        test_ln = Line(locs, 5)
        self.assertTrue(test_ln.weight == 5)
        self.assertTrue(test_ln.location[0].lat_deg == 52.416801)
        self.assertTrue(test_ln.location[0].lon_deg == -4.091099)
        self.assertTrue(test_ln.location[1].lat_deg == 52.415603)
        self.assertTrue(test_ln.location[1].lon_deg == -4.090702)
        self.assertTrue(test_ln.closest_point(loc3) == loc2)
        self.assertTrue(test_ln.closest_point(loc4) == loc1)
        self.assertFalse(test_ln.closest_point(loc2) == loc1)
        print test_ln.closest_point(loc1).lat_deg #TODO investigate why this fails
        print test_ln.closest_point(loc1).lon_deg
        self.assertTrue(test_ln.closest_point(loc1) == loc1)
        
        
        #test closest_point with midway points
        
        #test get_dist_to
        
    def test_Point(self):
        loc1 = Location(52.416801,-4.091099)
        loc2 = Location(52.415603,-4.090702)
        test_pt = Point(loc1, 5)
        self.assertTrue(test_pt.weight == 5)
        self.assertTrue(test_pt.location.lat_deg == 52.416801)
        self.assertTrue(test_pt.location.lon_deg == -4.091099)
        self.assertTrue(test_pt.get_dist_to(loc2) == dist_between(loc1,loc2))
        
        
    def test_Plane(self):
        loc1 = Location(52.416801,-4.091099)
        loc2 = Location(52.415603,-4.090702)
        
        test_pl = Plane(0, 4)
        vec = test_pl.get_vector()
        vec2 = np.array([0.000000,4.000000])
        self.assertTrue(vec[0]==vec2[0] and vec[1]==vec2[1] )
        
        test_pl2 = Plane(180, 4)
        vec3 = test_pl2.get_vector()
        vec4 = np.array([0.000000,-4.000000])
        self.assertTrue(vec3[0]==vec4[0] and vec3[1]==vec4[1] )
        
        test_pl2 = Plane(90, 4)
        vec3 = test_pl2.get_vector()
        vec4 = np.array([4.000000,0.000000])
        self.assertTrue(vec3[0]==vec4[0] and vec3[1]==vec4[1] )
        
      
tests = unittest.TestLoader().loadTestsFromTestCase(TestVectors)
unittest.TextTestRunner(verbosity=2).run(tests)
