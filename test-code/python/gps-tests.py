import numpy as np
import sys
sys.path.insert(0, 'git/AqASS/python-code/')
from main import *
import unittest

class TestGPS(unittest.TestCase):
    def test_GPS_to_dist(self):
        loc1 = Location(52.416801,-4.091099)
        loc2 = Location(52.415603,-4.090702)
        #print GPS_to_dist(loc1,loc2)
        self.assertTrue(GPS_to_dist(loc1,loc2) ==135.9 )
    def test_dist_to_GPS(self):
        loc1 = Location(52.416801,-4.091099)
        loc2 = Location(52.415603,-4.090702)
        self.assertTrue(dist_to_GPS(loc1, 135.9, 0) == loc2)

tests = unittest.TestLoader().loadTestsFromTestCase(TestGPS)
unittest.TextTestRunner(verbosity=2).run(tests)
