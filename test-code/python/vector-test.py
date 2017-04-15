import numpy as np
import sys
sys.path.insert(0, '/home/lizzie/git/AqASS/python-code')
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
        pass
      
tests = unittest.TestLoader().loadTestsFromTestCase(TestVectors)
unittest.TextTestRunner(verbosity=2).run(tests)
