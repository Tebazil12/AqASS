# AqASS
Aquatic Area Scanning System

A control system for a motor boat to make it autonomously scan a body of water. 
Multiple different behaviours can be written for this system but two are included
here; navigating to a single point, and navigating to a series of points.

This code is designed to be run on a motor-powered boat. The python code has been 
developed for a pi3, and the arudino code has been developed for a moteino, 
but this code will likely run on similar hardware.

## How to use
Before this program is run, all hardware must be connected (most importantly the 
compass and GPS).

Once all hardware is connected, start the Pi and load the Arduino code 
(arduino-code/src/src/src.ino) onto the Arduino. If the compass libraries are
not recognised you may need to tell the ArduinoIDE that they can be found in
arduino-code/lib . In its default state the Arduino will not print anything 
when the code is run; printing can be turned on to debug the code, but this
will prevent proper communication with the Pi so MUST be turned off before
running the code for real. 

Before running the code on the Pi, you must first update the water.csv, 
objects.csv and waypoints.csv files to include the GPS co-ordinates of the
area of water you wish to scan, any objects in the water (or points to be
avoided) and the points you wish the boat to go to respectively. 

To run the code on the Pi, check which USB ports the compass and arduino are 
located on and update the main.py and run-code.sh files with the appropriate 
ports. You can then run the code by running the run_code.sh file.

Every time the main.py file is run, there will be information printed in the 
log.csv file about where it was located at what time. You may want to copy this 
elsewhere after each run and empty it before the next run.
