#!/bin/bash
#sudo lsusb
ls /dev/ttyUSB*

#sudo systemctl stop gpsd.socket
#sudo systemctl disable gpsd.socket
#sudo gpsd /dev/ttyUSB1 -F /var/run/gpsd.sock
#sudo gpsd -D 5 -V -n /dev/ttyUSB1

#sleep 5
ls
cd python-code/
echo -e Yup
python main.py
echo killing gpsd...
sudo killall gpsd
echo -e Done