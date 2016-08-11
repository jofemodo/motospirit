#!/usr/bin/python3
# -*- coding: utf-8 -*-
#********************************************************************
# MOTOSPIRIT PROJECT: MONITOR DISPLAY
#--------------------------------------------------------------------
# mspanel.py: Main program
#--------------------------------------------------------------------
# Copyright (C) 2016 Fernando Moyano <jofemodo@zynthian.org>
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

import sys
import can
import datetime
#import pycanopen
from PyQt4 import QtGui
from PyQt4 import QtCore
import MainWindow

class mspanel(QtGui.QMainWindow):

	color_blue = "#0000ff"
	color_green = "#00f000"
	color_orange = "#f88000"
	color_red = "#f00000"

	canbus = None
	canbus_interface = 'vcan0'

	#logdir = "/home/pi/motospirit/log"
	logdir = "../log"
	logfd = None

	values = {}

	def __init__(self):
		super(mspanel, self).__init__()
		self.ui = MainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.setInitValues()
		self.initLogFile()
		self.initCanBusUpdater()

	def __del__(self):
		self.logfd.close()

	def XsetInitValues(self):
		self.values['RPM']=4869
		self.values['KMH']=135
		self.values['SOC']=87
		self.values['Tbat']=65
		self.values['Tdriver']=78
		self.values['Tengine']=42
		self.values['Vbat']=114
		self.values['Imax']=36
		self.values['Vmincell']=4.3
		self.values['Vmaxcell']=5.2
		self.values['Tmincell']=127
		self.values['Tmaxcell']=138

	def setInitValues(self):
		self.values['RPM']=1000
		self.values['KMH']=10
		self.values['SOC']=100
		self.values['Tbat']=10
		self.values['Tdriver']=10
		self.values['Tengine']=10
		self.values['Vbat']=115
		self.values['Imax']=0
		self.values['Vmincell']=4.5
		self.values['Vmaxcell']=4.5
		self.values['Tmincell']=10
		self.values['Tmaxcell']=10

	def initLogFile(self):
		ts=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		self.logfd = open(self.logdir+'/motospirit-'+ts+'.csv','w')
		self.logfd.write("RPM, KMH, SOC, Tbat, Tdriver, Tengine, Vbat, Imax, Vmincell, Vmaxcell, Tmincell, Tmaxcell\n")

	def initCanBusUpdater(self):
		self.canbus = can.interface.Bus(self.canbus_interface, bustype='socketcan')
		#self.canbus = CANopen.CANopen(self.canbus_interface)
		self.canbus_timer = QtCore.QTimer()
		self.canbus_timer.timeout.connect(self.canBusUpdater)
		self.canbus_timer.start(200)

	def canBusUpdater(self):
		self.getCanBusValues()
		self.updateUi()
		self.logValues()

	def updateUi(self):
		self.setRPMValue()
		self.setKMHValue()
		self.setSOCValue()
		self.setTbatValue()
		self.setTdriverValue()
		self.setTengineValue()
		self.setVbatValue()
		self.setImaxValue()
		self.setVmincellValue()
		self.setVmaxcellValue()
		self.setTmincellValue()
		self.setTmaxcellValue()

	def logValues(self):
		self.logfd.write(
			str(self.values['RPM'])+','+
			str(self.values['KMH'])+','+
			str(self.values['SOC'])+','+
			str(self.values['Tbat'])+','+
			str(self.values['Tdriver'])+','+
			str(self.values['Tengine'])+','+
			str(self.values['Vbat'])+','+
			str(self.values['Imax'])+','+
			str(self.values['Vmincell'])+','+
			str(self.values['Vmaxcell'])+','+
			str(self.values['Tmincell'])+','+
			str(self.values['Tmaxcell'])+'\n'
		)

	def parseDataInt8(self, data, i=0):
		v=data[i]
		if (v >> 7): v=(-0x80 + (v & 0x7f))
		return v

	def parseDataUInt8(self, data, i=0):
		return data[i]

	def parseDataInt16(self, data, i=0):
		v=data[i] | (data[i+1] << 8)
		if (v >> 15): v=(-0x8000 + (v & 0x7fff))
		return v

	def parseDataUInt16(self, data, i=0):
		v=data[i] | (data[i+1] << 8)
		return v

	#------------------------------------
	# Controller => openCAN dictionary
	#------------------------------------
	# RPS => 3A90.2 (Unsigned32)
	#			=> 380B.4
	#			=> 3A91.2
	#	RPM => 606C.0 (Integer32/Integer16) => PDO
	#			=> 706C.0 (Integer32) => PDO
	# Tengine => 4600.3 (Integer16) => PDO
	#					=> 4700.3 (Integer16) => PDO
	# Tdriver	=>
	#------------------------------------
	# BMS => STPM (1 sec), start from 620
	#------------------------------------
	# Vbat 			=> 623.0 (2) => BigEndian
	# Vmincell	=> 623.2 => 0.1V
	# Vmaxcell 	=> 623.4 => 0.1V
	# Imax			=> 624.0 (2) => BigEndian, 2's complement
	# SOC				=> 626.0 (1)
	# Tbat			=> 627.0 (1) => 2's complement
	# Tmincell	=> 627.2 (1) => 2's complement
	# Tmaxcell	=> 627.4 (1) => 2's complement
	#------------------------------------	
	def getCanBusValues(self):
		while True:
			msg = self.canbus.recv(0.0)
			if msg is None: break
			print("BusCan Message => " + str(msg))
			#RBPi GPIO Sensors PDOs
			if msg.arbitration_id==0x388:
				self.values['KMH']=self.parseDataInt16(msg.data,0)
			#Engine Driver PDOs
			if msg.arbitration_id==0x222:
				self.values['Tdriver']=self.parseDataInt8(msg.data,1)
				self.values['RPM']=self.parseDataInt16(msg.data,4)
				self.values['KMH']=0.037*self.values['RPM']
			elif msg.arbitration_id==0x223:
				self.values['Tengine']=self.parseDataInt16(msg.data,0)
			#BMS PDOs
			elif msg.arbitration_id==0x623:
				self.values['Vbat']=self.parseDataUInt16(msg.data,0)
				self.values['Vmincell']=0.1*self.parseDataUInt8(msg.data,2)
				self.values['Vmaxcell']=0.1*self.parseDataUInt8(msg.data,4)
			elif msg.arbitration_id==0x624:
				self.values['Imax']=self.parseDataInt16(msg.data,0)
			elif msg.arbitration_id==0x626:
				self.values['SOC']=self.parseDataUInt8(msg.data,0)
			elif msg.arbitration_id==0x627:
				self.values['Tbat']=self.parseDataInt8(msg.data,0)
				self.values['Tmincell']=self.parseDataInt8(msg.data,2)
				self.values['Tmaxcell']=self.parseDataInt8(msg.data,4)

	def setRPMValue(self, value=None):
		if value is None: value=self.values['RPM']
		if value>=4800: color=self.color_red
		elif value>=3000: color=self.color_orange
		elif value>=1500: color=self.color_green
		else: color=self.color_blue
		self.ui.progressBar_RPM.setProperty("value", value)
		self.setProgressBarColor(self.ui.progressBar_RPM, color)

	def setKMHValue(self, value=None):
		if value is None: value=self.values['KMH']
		self.ui.lcdNumber_KMH.setProperty("value", value)

	def setSOCValue(self, value=None):
		if value is None: value=self.values['SOC']
		if value>=90: color=self.color_green
		elif value>=50: color=self.color_orange
		else: color=self.color_red
		self.ui.progressBar_SOC.setProperty("value", value)
		self.ui.lcdNumber_SOC.setProperty("value", value)
		self.setProgressBarColor(self.ui.progressBar_SOC, color)

	def setTbatValue(self, value=None):
		if value is None: value=self.values['Tbat']
		if value>=120: color=self.color_red
		elif value>=90: color=self.color_orange
		elif value>=50: color=self.color_green
		else: color=self.color_blue
		self.ui.progressBar_Tbat.setProperty("value", value)
		self.ui.lcdNumber_Tbat.setProperty("value", value)
		self.setProgressBarColor(self.ui.progressBar_Tbat, color)

	def setTdriverValue(self, value=None):
		if value is None: value=self.values['Tdriver']
		if value>=75: color=self.color_red
		elif value>=50: color=self.color_orange
		elif value>=25: color=self.color_green
		else: color=self.color_blue
		self.ui.progressBar_Tdriver.setProperty("value", value)
		self.ui.lcdNumber_Tdriver.setProperty("value", value)
		self.setProgressBarColor(self.ui.progressBar_Tdriver, color)

	def setTengineValue(self, value=None):
		if value is None: value=self.values['Tengine']
		if value>=120: color=self.color_red
		elif value>=90: color=self.color_orange
		elif value>=50: color=self.color_green
		else: color=self.color_blue
		self.ui.progressBar_Tengine.setProperty("value", value)
		self.ui.lcdNumber_Tengine.setProperty("value", value)
		self.setProgressBarColor(self.ui.progressBar_Tengine, color)

	def setVbatValue(self, value=None):
		if value is None: value=self.values['Vbat']
		self.ui.lcdNumber_Vbat.setProperty("value", value)

	def setImaxValue(self, value=None):
		if value is None: value=self.values['Imax']
		self.ui.lcdNumber_Imax.setProperty("value", value)

	def setVmincellValue(self, value=None):
		if value is None: value=self.values['Vmincell']
		self.ui.lcdNumber_Vmincell.setProperty("value", value)

	def setVmaxcellValue(self, value=None):
		if value is None: value=self.values['Vmaxcell']
		self.ui.lcdNumber_Vmaxcell.setProperty("value", value)

	def setTmincellValue(self, value=None):
		if value is None: value=self.values['Tmincell']
		self.ui.lcdNumber_Tmincell.setProperty("value", value)

	def setTmaxcellValue(self, value=None):
		if value is None: value=self.values['Tmaxcell']
		self.ui.lcdNumber_Tmaxcell.setProperty("value", value)

	def setProgressBarColor(self, pgobj, color="#00c000"):
		st = ("QProgressBar::chunk {"
			"background-color: "+color+";"
			"border-radius: 8px;"
			"}"
			"QProgressBar {"
			"border: 1px solid #c0c0c0;"
			"border-radius: 8px;"
			"text-align: center;"
			"color: #ffffff;"
			"background-color: #e0e0e0;"
			"}")
		pgobj.setStyleSheet(st)

app = QtGui.QApplication(sys.argv)

my_mspanel = mspanel()
my_mspanel.show()

sys.exit(app.exec_())
