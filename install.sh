#!/bin/bash
#******************************************************************************
# MOTOSPIRIT PROJECT: Motospirit Display Install Script
# 
# Configure and Install all Software needed by MotoSpirit Display
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

# Requirements ...
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pyqt4 pyqt4-dev-tools libcanberra-gtk0 mercurial automake m4 cmake can-utils joe tree fbi i2c-tools libi2c-dev

# Install python-can
cd $MSDIR/src
hg clone https://bitbucket.org/hardbyte/python-can
cd python-can
sudo python3 setup.py install

# Install libcanopen
cd $MSDIR/src
git clone https://github.com/rscada/libcanopen.git
cd libcanopen
rm -f ./depcomp
ln -s /usr/share/automake-1.14/depcomp .
./configure
make
sudo make install
cd python
sudo python3 ./setup.py install
sudo ldconfig

# Install fonts
sudo cp $MSDIR/src/fonts/* /usr/local/share/fonts
sudo fc-cache -fv

# Add user pi to video group
sudo useradd -G video pi

# Copy xinitrc
cp -f $MSDIR/config/xinitrc ~/.xinitrc
cp -f $MSDIR/config/xinitrc ~/.xsession

# Splash Screen
sudo cp -f $MSDIR/config/asplashscreen /etc/init.d/asplashscreen 
sudo ln -s /etc/init.d/asplashscreen /etc/rcS.d/S01asplashscreen
sudo systemctl enable asplashscreen

# Make
cd $MSDIR/src
make

cd $MSDIR

