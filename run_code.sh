#!/bin/bash
#ls /dev/ttyUSB*


#sudo pkill gpsd
#sudo systemctl disable gpsd.socket		
#sudo gpsd /dev/ttyUSB1 -F /var/run/gpsd.sock

gpsd /dev/ttyUSB0

cd python-code/
python main.py

