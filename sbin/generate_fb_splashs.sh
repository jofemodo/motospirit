#!/bin/bash

MSDIR=~/motospirit

sudo fbi --noverbose -vt 2 -d /dev/fb0 $MSDIR/src/img/logo_motospirit_800x450.png
sudo cat /dev/fb0 > $MSDIR/src/img/fb_motospirit.raw

sudo fbi --noverbose -vt 2 -d /dev/fb0 $MSDIR/src/img/logo_motospirit_error_800x450.png
sudo cat /dev/fb0 > $MSDIR/src/img/fb_motospirit_error.raw
