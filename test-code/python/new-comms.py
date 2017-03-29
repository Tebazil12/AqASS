import arduinoserial 
from time import sleep

arduino = arduinoserial.SerialPort('/dev/ttyUSB1', 9600)
arduino.write('h(890)')
sleep(0.5)
thing = arduino.read_until('\n')
print (thing)
arduino.write('h(89)')
sleep(5)
arduino.write('e')
thing2 = arduino.read_until('\n')
print (thing2)

