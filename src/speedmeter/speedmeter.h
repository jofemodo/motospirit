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

// pin => GPIO pin that receives the pulses
// mpp => meters/pulse for speed calculation
void init_speedmeter(unsigned int pin, float mpp);

// Returns speed in m/s
float get_speedmeter_value();

//-----------------------------------------------------------------------------
