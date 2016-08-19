#!/bin/bash
#******************************************************************************
# MOTOSPIRIT PROJECT: Motospirit Display Startup Script
# 
# Start all Services needed by MotoSpirit Display
# 
# Copyright (C) 2016 Fernando Moyano <jofemodo@zynthian.org>
#
#******************************************************************************
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE.txt file.
# 
#******************************************************************************

MOTOSPIRIT_DIR="/home/pi/motospirit"

#------------------------------------------------------------------------------
# Some Functions
#------------------------------------------------------------------------------

function screensaver_off() {
	# Don't activate screensaver
	xset s off
	# Disable DPMS (Energy Star) features.
	xset -dpms
	# Don't blank the video device
	xset s noblank
}

function scaling_governor_performance() {
	for cpu in /sys/devices/system/cpu/cpu[0-9]*; do 
		echo -n performance | tee $cpu/cpufreq/scaling_governor
	done
}

function splash_motospirit() {
	if [ -c /dev/fb0 ]; then
		cat $MOTOSPIRIT_DIR/src/img/fb_motospirit.raw > /dev/fb0
	fi  
}

function splash_motospirit_error() {
	if [ -c /dev/fb0 ]; then
		cat $MOTOSPIRIT_DIR/src/img/fb_motospirit_error.raw > /dev/fb0
	fi  
}

#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------

#CANDEV="vcan0"
CANDEV="can0"

cd $MOTOSPIRIT_DIR/src

screensaver_off
scaling_governor_performance

xhost +
unclutter -root -idle 0 & 

while true; do
	# Start Motospirit Main Program
	sudo ./mspanel.py
	status=$?

	# Proccess output status
	case $status in
		0)
			splash_motospirit
			poweroff
			break
		;;
		*)
			splash_motospirit_error
			sleep 2
			splash_motospirit
		;;
	esac  
done

#------------------------------------------------------------------------------
