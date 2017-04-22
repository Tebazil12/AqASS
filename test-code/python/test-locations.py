import numpy as np
import sys
sys.path.insert(0, '../../python-code')
from locations import *
import unittest

class TestLocs(unittest.TestCase):
    #loc_a = Location(52.416801,-4.091099)
    #loc_b = Location(52.426801,-4.092099)
    def test_dist_between(self):
        print 'test'
        loc1 = Location(52.416801,-4.091099)
        loc2 = Location(52.415603,-4.090702)
        self.assertTrue(dist_between(loc1,loc2) ==135.9 )
        #loc_a = Location(52.416801,-4.091099)
        #loc_b = Location(52.416805,-4.091095)
        #print dist_between(loc_a,loc_b)
        #self.assertTrue(dist_between(loc_a,loc_b) == 1 )
    #def test_dist_to_GPS(self):
     #   loc1 = Location(52.416801,-4.091099)
      #  loc2 = Location(52.415603,-4.090702)
       # self.assertTrue(dist_between(loc1, 135.9, 0) == loc2)

tests = unittest.TestLoader().loadTestsFromTestCase(TestLocs)
unittest.TextTestRunner(verbosity=2).run(tests)
