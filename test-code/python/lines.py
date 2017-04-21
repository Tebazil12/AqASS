#things = ['a','b','c','d','e','f' ]

#size = len(things)
#print size
#for i, thing in enumerate(things):
#    if i+1 == size:
#        print things[i], 'to', things[0]
#    else:
#        print things[i], 'to', things[i+1]
    

#import numpy as np
import sys
sys.path.insert(0, '../../python-code')
from vectors import *
from locations import *
WEIGHT_BOUNDRY = -5

def get_perim_lines(perimeter_locs):
    lines = []
    size = len(perimeter_locs)
    print size
    for i, thing in enumerate(perimeter_locs):
        if i+1 == size:
            print perimeter_locs[i], 'to', perimeter_locs[0]
            lines.append(Line([perimeter_locs[i],perimeter_locs[0]], WEIGHT_BOUNDRY))
        else:
            print perimeter_locs[i], 'to', perimeter_locs[i+1]
            ln = Line([perimeter_locs[i],perimeter_locs[i+1]], WEIGHT_BOUNDRY)
            print ln
            lines.append(ln)
    return lines

print 'start'
loc1 = Location(52.416801,-4.091099)
loc2 = Location(52.415603,-4.090702)
loc3 = Location(52.415602,-4.090701)
loc4 = Location(52.416802,-4.091200)
locs = [loc1,loc2,loc3,loc4]

stuff = get_perim_lines(locs)
print stuff

print'finish'
