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

## Extract from reference for memory download :
#52		UploadData (OS 2), UploadData740 (OS 3),
#		UploadData (OS 4)
#		Upload data from the SmartBox's memory
#Send		Byte 0 = 52
#		Byte 1 = start address to read (low byte)
#		Byte 2 = start address to read (high byte)
#		Byte 3 = length of data (low byte)
#		Byte 4 = length of data (high byte)
#Returns		Byte 0 - n = data

## Extract from SmartBox documentation regarding how memory is mapped :
#In the controller the maximum limit of RAM is &8000 (which is 32k),
#from &8000-&DFFF lies the memory mapped hardware, from &E000 to &FFF9 lies
#the OS and from &FFFA to &FFFF lies the 65c02 vectors.

# the ROM is between 0xE000 and 0xFFFF - so I'll download 8kbytes from 0xE000.

import eSB
import time
import os.path

eSB.open('/dev/ttyUSB0')

ROMVer = eSB.get_sb_ver()
print "Smart Box OS Version : " + ROMVer

if len(eSB.get_command_name(52)) > 1:
	#print "Command 52 is called : " + eSB.get_command_name(52)
	
	if eSB.ser.is_open:
		print "Downloading from E000 to FFFF..."
		eSB.ser.write(chr(52)+chr(0x00)+chr(0xE0)+chr(0x00)+chr(0x20))
		# cmd, start low, start high, len low, len high
		time.sleep(0.1)
		i = 0x2000
		theData = []
		while i >=1:
			if eSB.ser.inWaiting() > 0: # data available
				dataByte = eSB.ser.read(1)
				theData = theData + [dataByte]
				#print str(i) + " " + str(ord(dataByte))
				if i % 1024 == 0:
					print(0x2000-(i))
				i = i-1
	print
	print "Done."
	print "Writing to file..."
	
	n=0
	while os.path.exists("SB"+ROMVer+"-"+str(n)+".BIN"):
		n=n+1
	
	outputFile=open("SB"+ROMVer+"-"+str(n)+".BIN",'wb')
	outputByteArray = bytearray(theData)
	outputFile.write(outputByteArray)
	outputFile.close()
	
	if os.path.exists("SB"+ROMVer+"-"+str(n)+".BIN"):
		print "File Saved as : "+"SB"+ROMVer+"-"+str(n)+".BIN"
	else:
		print "There was an error saving the file in the current directory."
	
	#print x(theData)
	
print "Exiting..."
eSB.close()
print "Complete."

