#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import time

# Test drive Nixie tube driver chip K155D1
# Letters map to decoder input  lines A==Pin3, B==pin6, C==pin7 & D== pin4
#
# Truth Table (BDC really)
# A-B-C-D	output#	pin#
# 0-0-0-0	0	16
# 0-0-0-1	1	15
# 0-0-1-0	2	08
# 0-0-1-1	3	09
# 0-1-0-0	4	13
# 0-1-0-1	5	14
# 0-1-1-0	6	11
# 0-1-1-1	7	10
# 1-0-0-0	8	01
# 1-0-0-1	9	02

global GPIO_A
global GPIO_B
global GPIO_C
global GPIO_D

# Adjust for GPIO test setup
GPIO_A = 18
GPIO_B = 25
GPIO_C = 18
GPIO_D = 23


# Turn on pins associated with A, B, C, D inputs
#def bdc(a, b, c, d) :
#may have truth table wrong way round...
#not counting as first setup
def bdc(d, c, b, a) :
	print "A:", a, " B:", b, " C:", c, " D:", d
	GPIO.output (GPIO_A, True) if a else GPIO.output (GPIO_A, False)
	GPIO.output (GPIO_B, True) if b else GPIO.output (GPIO_B, False)
	GPIO.output (GPIO_C, True) if c else GPIO.output (GPIO_C, False)
	GPIO.output (GPIO_D, True) if d else GPIO.output (GPIO_D, False)
	time.sleep (3)
	

# Validate command line
argcnt = len(sys.argv)
if argcnt != 1 and argcnt != 5:
	sys.exit("Invalid args: No args to count, or 4 individual 0/1s to represent A, B, C, D")


# Initialise GPIO 
GPIO.setmode (GPIO.BCM)
GPIO.cleanup()
GPIO.setup (GPIO_A, GPIO.OUT)
GPIO.setup (GPIO_B, GPIO.OUT)
GPIO.setup (GPIO_C, GPIO.OUT)
GPIO.setup (GPIO_D, GPIO.OUT)

try:
	if argcnt == 1:
		for r in list(range(10)) :
			bdc( r&8, r&4, r&2, r&1 )
			print "counter r=", r, "r&2=", r&2, "r&2>>1=", r&2>>1
	else:
		bdc(	int(sys.argv[1]),
			int(sys.argv[2]),
			int(sys.argv[3]),
			int(sys.argv[4]))

except KeyboardInterrupt:
	pass
except:
	pass
GPIO.cleanup()
