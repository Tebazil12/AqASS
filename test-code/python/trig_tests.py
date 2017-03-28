import numpy as np

def wrap_degrees(angle):
    while angle<0:
        angle += 360
    angle = angle % 360
    return angle

print "++"
print wrap_degrees(np.degrees(np.arctan2(150,100)))
#print wrap_degrees(np.degrees(np.arctan(150/100.0)))

print "-+"
print wrap_degrees(np.degrees(np.arctan2(-150,100)))
#print wrap_degrees(np.degrees(np.arctan(-150/100.0)))

print "+-"
print wrap_degrees(np.degrees(np.arctan2(150,-100)))
#print wrap_degrees(np.degrees(np.arctan(150/-100.0)))

print "--"
print wrap_degrees(np.degrees(np.arctan2(-150,-100)))
#print wrap_degrees(np.degrees(np.arctan(-150/-100.0)))
