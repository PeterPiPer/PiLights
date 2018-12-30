#!/usr/bin/python

# Playtime with DS1307 realtime clock and the I2C interface
# Need to create get & set functions (once I've found my way around).

import smbus as smbus
import time as time


print "Hello i2c world"

# DS1307 i2c address from datasheet
clock_addr = 0b1101000
# Combine address with the read/write bit to form the initial message byte
#smbus imnterface doesn;'t work quite as i'd expect, DS1307 dfocs say first worf is (address <<)|1 for write, but first arg must be the device address
clock_read = (clock_addr<<1)| 0
clock_write = (clock_addr<<1)| 1

#print("Dev address ", bin(clock_addr), " ", clock_addr )
#print( "read ", bin(clock_read) )
#print( "write ", bin(clock_write) )

def set_time(bus) :
#have tpo set CH bit @0 to 0 to start the clock
	bus.write_byte_data(clock_addr, 0, 0)
	

def read_time(bus):
	sec = clock_bus.read_byte_data(clock_addr, 0)
	min = clock_bus.read_byte_data(clock_addr, 1)
	hour = clock_bus.read_byte_data(clock_addr, 2)
	day = clock_bus.read_byte_data(clock_addr, 3)
	date = clock_bus.read_byte_data(clock_addr, 4)
	month = clock_bus.read_byte_data(clock_addr, 5)
	year = clock_bus.read_byte_data(clock_addr, 6)
	
	#print( "sec ", bin(sec) )
	#print( "min ", bin(min) )
	#print( "hour ", bin(hour) )
	#print( "day ", bin(day) )
	#print( "date ", bin(date) )
	#print( "month ", bin(month) )
	#print( "year ", bin(year) )
	print( bin(year), "|", bin(month), "|", bin(date), "|", bin(day), " ", bin(hour), ":", bin(min), ":", bin(sec) )


#Initialise I2C, for channel 1 that is connected to te GPIO pins
# IO error wity hchannel 1, use 0 - Check against docs for more info
clock_bus = smbus.SMBus(0)

while True:
	read_time(clock_bus)
	time.sleep(5)

#set_time(clock_bus)

