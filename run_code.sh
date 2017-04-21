#!/bin/bash
sudo gpsd -D 5 -V -n /dev/ttyUSB1
ls
cd python-code/
echo -e Yup
python main.py
echo -e Done