#!/usr/bin/python

# Playtime with DS1307 realtime clock and the I2C interface
# Need to create get & set functions (once I've found my way around).

import smbus as smbus

print "Hello i2c world"

# DS1307 i2c address from datasheet
clock_addr = 0b1101000
# Combine address with the read/write bit to form the initial message byte
clock_read = (clock_addr<<1)| 0
clock_write = (clock_addr<<1)| 1


#print( "read ", bin(clock_read) )
#print( "write ", bin(clock_write) )

#Initialise I2C, for channel 1 that is connected to te GPIO pins
clock_bus = smbus.SMBus(1)


sec = clock_bus.read_i2c_block_data(clock_read, 0, 1) 
min = clock_bus.read_i2c_block_data(clock_read, 1, 1) 
hour = clock_bus.read_i2c_block_data(clock_read, 2, 1) 
day = clock_bus.read_i2c_block_data(clock_read, 3, 1) 
date = clock_bus.read_i2c_block_data(clock_read, 4, 1) 
month = clock_bus.read_i2c_block_data(clock_read, 5, 1) 
year = clock_bus.read_i2c_block_data(clock_read, 6, 1) 

print( "sec ", bin(sec) )
print( "min ", bin(min) )
print( "hour ", bin(hour) )
print( "day ", bin(day) )
print( "date ", bin(date) )
print( "month ", bin(month) )
print( "year ", bin(year) )
