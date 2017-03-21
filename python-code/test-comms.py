#import numpy as np
#import matplotlib.pyplot as plt

import serial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
#print(ser.name)         # check which port was really used
ser.write(b'e')     # write a string
#ser.close()             # close port
x = ser.readline()
print('the arduino said: ',x)
print('finish')
