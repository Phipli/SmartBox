# Smart Box Interface Library
# By Phil
# http://stuffandnonsense.elephantandchicken.co.uk
# 20200307
# This is an early development version
# of a python module designed to control the
# Economatics Smart Box
# Testing is conducted on an "SB-04"

import time
import serial

libVersion = "v0.01a - Phil - http://stuffandnonsense.elephantandchicken.co.uk"
ser = None

def open(port):
	global ser
	ser = serial.Serial(port, 9600, timeout=1)
	return ser.is_open

def close():
	global ser
	if ser.is_open:
		ser.close()
	ser = None

def flush():
	global ser
	if ser.is_open:
		readTest = ""
		while ser.inWaiting() > 0:
                        readText += ser.read(1)

def get_sb_copyright():
	global ser
	ser.write(chr(9))
	time.sleep(0.1)
	readText = ""
	print "Debug note : There is something odd about this response..."
	while ser.inWaiting() > 0:
		readText += ser.read(1)
		#time.sleep(0.1)
	return readText

def get_sb_ver():
	global ser
	readValue = 0.0
	if ser.is_open:
		ser.write(chr(1))
		time.sleep(0.1)
		readByteL = ord(ser.read(1))
		#time.sleep(0.1)
		readByteH = ord(ser.read(1))
		readByteH *= 256
		readValue = readByteH+readByteL
	else:
		raise NameError('Serial connection not open - try calling eSB.open(xyz) first')
	return str(float(readValue)/1000)

def get_command_name(cmd):
	global ser
	readText = ""
	if ser.is_open:
		ser.write(chr(4)+chr(cmd))
        	time.sleep(0.1)
        	#print "Debug note : There is something odd about this response..."
        	while ser.inWaiting() > 0:
        	        readText += ser.read(1)
        	        #time.sleep(0.1)
	elif not(ser.is_open):
		raise NameError('Serial connection not open - try calling eSB.open(xyz) first')
        return readText

def status():
	global ser
	global libVersion
	msg = "Module version : "+libVersion+"\n"
	if ser.is_open:
		msg += "Port is Open\nSystem version : "
		msg += getSBVer()
		return msg
	elif not(ser.is_open):
		#raise NameError('Serial connection not open - try calling eSB.open(xyz) first')
		return "Port is Not Open"

def d_out_on_all():
	global ser
	if ser.is_open:
                #print "Sending All On"
                ser.write(chr(20)+chr(255))
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def d_out_off_all():
	global ser
        if ser.is_open:
                #print "Sending All Off"
                ser.write(chr(20)+chr(0))
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def d_out_all(val1):
	global ser
	if ser.is_open:
		#print "Sending ",val1
		ser.write(chr(20)+chr(val1))
	else:
		raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def d_out_on_chn(chn):
	global ser
	if ser.is_open:
		ser.write(chr(28)+chr(chn+1))
	else:
		raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def d_out_off_chn(chn):
        global ser
        if ser.is_open:
                ser.write(chr(29)+chr(chn+1))
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def d_out_chn(chn, val1):
        global ser
        if ser.is_open:
		if val1==0:
			ser.write(chr(29)+chr(chn+1))
		elif val1==1:
			ser.write(chr(28)+chr(chn+1))
		else:
			raise NameError('Digital outputs need to be either 0 or 1')
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def d_in_all():
        global ser
	readByte = -1
        if ser.is_open:
                ser.write(chr(90))
		time.sleep(0.1)
		readByte = ord(ser.read(1))
		while ser.inWaiting() > 0:
                        print "Weird other data : " + str(ord(ser.read(1))) # no idea why these exist
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')
	return readByte

def d_in_chn(chn):
	global ser
	readByte = -1
	if ser.is_open:
                ser.write(chr(91)+chr(chn+1))
                time.sleep(0.1)
                readByte = ord(ser.read(1))
                while ser.inWaiting() > 0:
                        print "Weird other data : " + str(ord(ser.read(1))) # no idea why these exist
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')
        return readByte

def m_fwd_chn(chn):
	global ser
	if ser.is_open:
		ser.write(chr(12)+chr(chn))
	else:
		raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def m_bkw_chn(chn):
        global ser
        if ser.is_open:
                ser.write(chr(13)+chr(chn))
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def m_stp_chn(chn):
        global ser
        if ser.is_open:
                ser.write(chr(14)+chr(chn))
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

#def m_spd_chn(spd):
#        global ser
#        if ser.is_open:
#                ser.write(chr(15)+chr(spd))
#        else:
#                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def read_byte(addr):
	global ser
	if ser.is_open:
		highB = addr/256
		lowB = addr-(highB*256)
		ser.write(chr(56)+chr(lowB)+chr(highB))
		time.sleep(0.01)
		#while ser.inWaiting() > 0:
                readByte = ord(ser.read(1))
		return readByte
	else:
		raise NameError('Serial connection not open - try calling eSB.open(xyz) first')

def a_sensors():
	global ser
	analogue = []
	if ser.is_open:
		ser.write(chr(43))
		time.sleep(0.1)
		#sen = ("A","B","C","D")
		i=0
                while ser.inWaiting() > 0:
                        #print "Sensor " + sen[i] + " : " + str(ord(ser.read(1)))
			analogue.append(str(ord(ser.read(1))))
			i+=1
	return analogue

def a_sensors_new():
        global ser
	analogue = []
        if ser.is_open:
                ser.write(chr(23))
                time.sleep(0.1)
                #sen = ("A","B","C","D")
                i=0
                while ser.inWaiting() > 0:
                        #print "Sensor " + sen[i] + " : " + str(ord(ser.read(1))) # no idea why these exist
                        analogue.append(str(ord(ser.read(1))))
			i+=1
	return analogue

def a_in_chn(chn):
        global ser
	# for now, I'm going to make it work at low resolution for simplicity
        readByte = -1
        if ser.is_open:
		ser.write(chr(45)) # set to 8 bit mode
		time.sleep(0.1)
                ser.write(chr(40)+chr(chn))
                time.sleep(0.1)
                readByte = ord(ser.read(1))
                while ser.inWaiting() > 0:
                        print "Weird other data : " + str(ord(ser.read(1))) # no idea why these exist
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')
        return readByte

def a_in_f_chn(chn):
        global ser
        # for now, I'm going to make it work at low resolution for simplicity
        readByte = -1
        if ser.is_open:
                ser.write(chr(45)) # set to 8 bit mode
                time.sleep(0.1)
                ser.write(chr(42)+chr(chn))
                time.sleep(0.1)
                readByte = ord(ser.read(1))
                while ser.inWaiting() > 0:
                        print "Weird other data : " + str(ord(ser.read(1))) # no idea why these exist
        else:
                raise NameError('Serial connection not open - try calling eSB.open(xyz) first')
        return readByte

def a_sensor_table(val1):
        global ser
        ser.write(chr(25)+chr(val1))
        time.sleep(0.5)
        readText = ""
        #print "Debug note : There is something odd about this response..."
        while ser.inWaiting() > 0:
                readText += ser.read(1)
                #time.sleep(0.1)
        return readText

