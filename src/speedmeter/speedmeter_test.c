/*
 * ******************************************************************
 * SPEEDMETER PROJECT: Speedmeter Library Tests
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
#include <unistd.h>

#include "speedmeter.h"

int main() {
	printf("INITIALIZING SPEEDMETER LIBRARY!\n");
	init_speedmeter(0,1);

	printf("TESTING ...\n");
	while(1) {
		printf("SPEED = %f\n", get_speedmeter_value());
		usleep(500000);
	}

	return 0;
}
