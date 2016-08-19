/*
 * ******************************************************************
 * MOTOSPIRIT PROJECT: SpeedMeter Library
 * 
 * Library for calculating speed from pulses in a GPIO input.
 * 
 * Copyright (C) 2016 Fernando Moyano <jofemodo@zynthian.org>
 *
 * ******************************************************************
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * For a full copy of the GNU General Public License see the LICENSE.txt file.
 * 
 * ******************************************************************
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#ifdef HAVE_WIRINGPI_LIB
	#include <wiringPi.h>
	#include <mcp23008.h>
#else
	#include "wiringPiEmu.h"
#endif

#include "speedmeter.h"

//-----------------------------------------------------------------------------
// Variables
//-----------------------------------------------------------------------------

unsigned int sm_pin;
unsigned long int last_tsns;
unsigned long int last_dtns;
float sm_mpp;
float sm_mps;

//-----------------------------------------------------------------------------
// Interrupt Function => Recalculate speed every pulse 
//-----------------------------------------------------------------------------

void update_speedmeter() {
	struct timespec ts;
	unsigned long int tsns;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	tsns=ts.tv_sec*1000000 + ts.tv_nsec/1000;
	last_dtns=tsns-last_tsns;
	last_tsns=tsns;
	sm_mps=1000000*sm_mpp/last_dtns;
	//printf("SPEEDMETER PULSE! => %f m/s\n",sm_mps);
}

//-----------------------------------------------------------------------------
// Library Initialization
//-----------------------------------------------------------------------------

// pin => GPIO pin that receives the pulses
// mpp => meters/pulse for speed calculation
void init_speedmeter(unsigned int pin, float mpp) {
	sm_pin=pin;
	sm_mpp=mpp;
	sm_mps=0.0;
	last_tsns=0;
	last_dtns=1e9;
	
	wiringPiSetup();
	pinMode(sm_pin, INPUT);
	pullUpDnControl(sm_pin, PUD_UP);
	//wiringPiISR(sm_pin,INT_EDGE_BOTH, update_speedmeter);
	wiringPiISR(sm_pin,INT_EDGE_RISING, update_speedmeter);
}

// Returns speed in m/s
float get_speedmeter_value() {
	struct timespec ts;
	unsigned long int tsns;
	unsigned long int dtns;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	tsns=ts.tv_sec*1000000 + ts.tv_nsec/1000;
	dtns=tsns-last_tsns;
	if (dtns>last_dtns) sm_mps=1000000*sm_mpp/dtns;
	return sm_mps;
}

//-----------------------------------------------------------------------------
