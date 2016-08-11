#!/bin/bash
#******************************************************************************
# MOTOSPIRIT PROJECT: Motospirit Display Update Script
# 
# Update MotoSpirit Display software
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

MSDIR=~/motospirit

cd $MSDIR
git pull

# Install fonts
#sudo cp $MSDIR/src/fonts/* /usr/local/share/fonts
#sudo fc-cache -fv

# Copy xinitrc
cp -f $MSDIR/config/xinitrc ~/.xinitrc
cp -f $MSDIR/config/xinitrc ~/.xsession

# Splash Screen
#sudo cp -f $MSDIR/config/asplashscreen /etc/init.d/asplashscreen 
#sudo ln -s /etc/init.d/asplashscreen /etc/rcS.d/S01asplashscreen
#sudo systemctl enable asplashscreen

# Make
#cd $MSDIR/src
#make

cd $MSDIR

