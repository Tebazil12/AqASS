#!/bin/bash
#ls /dev/ttyUSB*

gpsd /dev/ttyUSB1

cd python-code/
python main.py

