#!/usr/bin/python3
# -*- coding: utf-8 -*-
#********************************************************************
# MOTOSPIRIT PROJECT: SPEEDMETER Python Wrapper
# 
# A Python wrapper for the SpeedMeter library
# 
# Copyright (C) 2016 Fernando Moyano <jofemodo@zynthian.org>
#
#********************************************************************
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
#********************************************************************

from ctypes import *
from os.path import dirname, realpath

#-------------------------------------------------------------------------------
# Zyncoder Library Wrapper
#-------------------------------------------------------------------------------

global lib_speedmeter
lib_speedmeter=None

def lib_speedmeter_init(pin, mpp):
	global lib_speedmeter
	try:
		lib_speedmeter=cdll.LoadLibrary(dirname(realpath(__file__))+"/build/libspeedmeter.so")
		lib_speedmeter.init_speedmeter(pin, c_float(mpp))
	except Exception as e:
		lib_speedmeter=None
		print("Can't init speedmeter library: %s" % str(e))
	return lib_speedmeter

def get_lib_speedmeter():
	return lib_speedmeter

def get_speedmeter_value():
	global lib_speedmeter
	func=lib_speedmeter.get_speedmeter_value
	func.restype=c_float
	return func()

#-------------------------------------------------------------------------------
