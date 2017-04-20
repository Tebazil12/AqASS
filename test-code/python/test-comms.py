#import numpy as np
#import matplotlib.pyplot as plt

#TODO find where example code came from
from time import sleep
import serial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
sleep(5)
#print(ser.name)         # check which port was really used

#for i in range(0,5):
thing = 'h(' + str(920) +')'
print(thing)
thing = thing.encode('utf-8')
#print(thing)
ser.write(thing)     # write a string
#ser.close()             # close port
x = ser.readline().strip()
#x = x.decode('utf-8')
print('the arduino said: ',x)
sleep(7)
print('finish')
ser.write(b'e')
x = ser.readline().strip()
y = x.decode('utf-8')
print('the arduino said: ',x)
#print('the arduino said: ',y)
ser.close() 
