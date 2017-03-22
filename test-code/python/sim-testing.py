import numpy as np
import matplotlib.pyplot as plt

# start the other thing running (the vectors pi stuff)

# fake the gps

# listen to what comes out of this script over serial/similar
# from that, get speed and desired heading

# now either represent the vector feild on graph (computationally heavy)
# or take time diff, draw point in direction (using speed = d/t)
time_previous = 0
time_current = None
coord_previous = None

while 1:
    # get speed and heading from pi thing
    time_diff = time_current - time_previous


    distance = speed * time_diff
    coord_current.x = coord_previous.x + distance*sin(heading)

    plt.plot(coord_current.x, coord_current.y) # maybe plot previous coord too if
                                                # this doesnt show on graph
                                            
    # at end of loop:
    # send current coord to pi as fake gps
    time_previous = time_current
    coord_previous = coord_current
    
    
