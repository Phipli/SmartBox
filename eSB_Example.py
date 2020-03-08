#!/usr/bin/python

# Smart Box Interface Library
# By Phil
# http://stuffandnonsense.elephantandchicken.co.uk
# 20200307
# This is an early development version
# of a python module designed to control the
# Economatics Smart Box
# Testing is conducted on an "SB-04"

# This file is an example using some functions from the library

import eSB
import time

eSB.open('/dev/ttyUSB0')

print "Smart Box OS Version : " + eSB.get_sb_ver()

print "Command 12 is called : " + eSB.get_command_name(12)

print "Turn all digital outpus on..."

eSB.d_out_on_all()

time.sleep(3)

print "Turn half of them off again..."

eSB.d_out_all(15)

time.sleep(3)

eSB.d_out_off_all()

try:
	while True:
		print "Press Ctrl-c to exit.   Digital Inputs : " + format(eSB.d_in_all(), '08b')
		time.sleep(1)
except KeyboardInterrupt:
	print "Exiting..."
	eSB.close()
	print "Done."

