#import numpy as np
#import matplotlib.pyplot as plt

#TODO find where example code came from
from time import sleep
import serial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print 5
sleep(1)
print 4
sleep(1)
print 3
sleep(1)
print 2
sleep(1)
print 1
sleep(1)

thing = 'h(' + str(920) +')'
print(thing)
thing = thing.encode('utf-8')
ser.write(thing)
x = ser.readline().strip() # removes \n and \r
print'the arduino said: ',x
print type(x)

#sleep(7)

thing2 = 'c'
print(thing2)
thing2 = thing2.encode('utf-8')
ser.write(thing2)
x = ser.readline().strip() # removes \n and \r
i = int(filter(str.isdigit, x)) # http://stackoverflow.com/questions/26825729/extract-number-from-string-python
print type(i)
print'the arduino said: ',x , i
print type(x)

print 'finish'
ser.write(b'e')
x = ser.readline().strip()
print 'the arduino said: ',x
ser.close()

