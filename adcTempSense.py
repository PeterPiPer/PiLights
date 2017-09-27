#!/usr/bin/python

import time as time
import RPi.GPIO as GPIO
import spidev

_DEBUG = True

# Temp Sesor TMP36GT9Z
# ADC via MPC3208 12bit 8 channel
# Comms over serial interface.
# MCP3208 Pin out as follows:
#	input0	1		16	VCC
#	input1	2		15	VDD (wire to VCC)
#	input0	3		14	Alt GND (wire to GND)
#	input0	4		13	CLK
#	input0	5		12	SO
#	input0	6		11	SI
#	input0	7		10	CC/xxx
#	input0	8		9	GND
# 
# looked at info from https://raspberrypi-aa.github.io/session3/spi.html
# This covers both spidev and 'bit banging' direct through GPIO, interesting
# if i want to lear all aspects of SPI protocol.

# Pi pins, and mapping to MC_P3208 pin
# GPIO-09 (MISO, master input slave output)
# GPIO-10 (MOSI, master output slave input )
# GPIO-11 (SCLK, blah )
# GPIO-01 (SCL, blah )
# Either 3.3 or 5 volts power, use 3.3
# GDN
# to get to SPI, using spidev module (not direct GPIO), enables SPI in raspi-config, does all the setup work


GPIO.setmode (GPIO.BCM)

#print "GPIO-09 MISO: Function 1. 40, 41? - ", GPIO.gpio_function(9)
#print "GPIO-10 MOSI: Function 0. 40, 41? - ", GPIO.gpio_function(10)
#print "GPIO-11 SCLK: Function 40/41? - ", GPIO.gpio_function(11)
#print "GPIO-01 clISO: Function 1? - ", GPIO.gpio_function(1)
GPIO.cleanup()



def bitDump(word, debug=False) :
	buf = [0,0,0,0,0,0,0,0]
	for i in range(8) :
		buf[7-i] = (word &2**i)>>i
	if (debug) :
		print "Word in: ", word, "bits: ", buf
	return buf
# End bitDump


# MCP3208 a 12 bit response, which will be in the lowest bits of the response
# response will follow the initiation, start, SGL/DIF, D2, D1, D0, so count
# back from end, 12 bits data,+ null Dout bit + 5 bits initiation == 18bits;
# must transmit 8bit/byte blocks, so 3 bytes required (24 bits).
# therefore to get the data we need in the right most bits
# bit position as follows (NB different clock edges for in/out
# 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
# D in aligned with falling enge clock
# 00 00 00 00 00 SB SD D2 D1 D0 -- -- -- -- --...
# D out  aligned with rising edge of clock
#                               nb 12 .. .. 09 .. .. .. 05 .. .. .. 01 00
# So pad input sequence with 5 0 bits before start to get output starting
# from end of 3 byte response.
#
def readChannel( spidev, channel, debug=False) :
	if (channel <0 or channel >7 ):
		return -1
	start=0x01
	# single source is 1, differentail 0
	singleDiff = 0x01

	b1 = ( start << 2 ) | (singleDiff <<1) | ((channel & 0x04)>>2)
	b2 = (channel & 0x03)<<6
	b3 = 0x00

	if (debug) :
		print "channel: ", channel
		print "write to adc:\t",bitDump(b1),", ",bitDump(b2),", ",bitDump(b3)
	
	# xfer2 keeps CS asserted for whole transfer (xfer reasserts 
	# CS after each byte
	x = spidev.xfer2( [b1, b2, b3 ] )
	if (debug) :
		print "xfer2 adc out:\t", bitDump(x[0]),", ",bitDump(x[1]),", ",bitDump(x[2])
	return x
#end readChannel


# From MCP3208 spec reults in mV AdcOutput=4096*Vin/Vref  
#
def processAdcValue( value, vref=3300, debug=False ) :
	res = ((value [1] & 0x0f)<< 8 ) | value[2]
	vin = res*vref/4096
	if (debug) :
		print "val[1]: ",  str(value[1]), " value[2]: ", str(value[2]), " output: ", res , " Vin: ", vin

	return vin
# end processAdcvalue


# From TMP36TG9 data sheet - reference value is 25C at 750mV, 10mv per 1C
#
def tempAdcToCelcius( vin , debug=False) :
	temp = -40 + (vin-100)/10.0

	if ( debug ) :
		print "Temperature is: ", temp, "'C ", 25-(750-vin)/10.0, "'C"

	return temp
# end tempAdcToCelcius




spi = spidev.SpiDev()
spi.open(0, 0)

try:
	while True:
		tempAdcToCelcius( processAdcValue( readChannel( spi, 2 ), 3310 ), _DEBUG)
		time.sleep(5)
	#while end

except KeyboardInterrupt:
	spi.close()
#end try

'''
for x in list(range(5)):
	GPIO.output (gpioTest, True)
	time.sleep (1)
	GPIO.output (gpioTest, False)
	time.sleep (1)
'''
