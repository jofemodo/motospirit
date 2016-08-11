#!/bin/bash

# Create a can network interface
#sudo /sbin/ip link add dev can0 type can bitrate 500000
#sudo /sbin/ip link set can0 up
sudo /sbin/ip link set can0 up type can bitrate 500000