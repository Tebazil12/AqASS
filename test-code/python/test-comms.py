#import numpy as np
#import matplotlib.pyplot as plt

from time import sleep
import serial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
#print(ser.name)         # check which port was really used

for i in range(0,5):
    thing = 'h(' + str(i*20) +')'
    print(thing)
    thing = thing.encode('utf-8')
    #print(thing)
    ser.write(thing)     # write a string
    #ser.close()             # close port
    #x = ser.readline()
    #print('the arduino said: ',x)
    sleep(7)
print('finish')
ser.write(b'e')
ser.close() 
