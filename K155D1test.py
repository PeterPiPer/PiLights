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


# Adjust for GPIO test setup
GPIO_A = 24
GPIO_B = 25
GPIO_C = 18
GPIO_D = 23

# Modify to test responsiveness to change
# Can see flicker at 0.006, flicker free at 0.001
# Nice scroll rate at 0.2 as can watch inputs cycle
SLEEP_TIME=0.2

# Turn on pins associated with A, B, C, D inputs
def bdc(a, b, c, d) :
	GPIO.output (GPIO_A, False) if a==0 else GPIO.output (GPIO_A, True)
	GPIO.output (GPIO_B, False) if b==0 else GPIO.output (GPIO_B, True)
	GPIO.output (GPIO_C, False) if c==0 else GPIO.output (GPIO_C, True)
	GPIO.output (GPIO_D, False) if d==0 else GPIO.output (GPIO_D, True)
	time.sleep (SLEEP_TIME)
	

# Validate command line
argcnt = len(sys.argv)
if argcnt != 1 and argcnt != 5:
	sys.exit("Invalid args: No args to count, or 4 individual 0/1s to represent A, B, C, D")


# Initialise GPIO 
GPIO.cleanup()
GPIO.setmode (GPIO.BCM)
GPIO.setup (GPIO_A, GPIO.OUT, False)
GPIO.setup (GPIO_B, GPIO.OUT, False)
GPIO.setup (GPIO_C, GPIO.OUT, False)
GPIO.setup (GPIO_D, GPIO.OUT, False)

try:
	if argcnt == 1:
		while True:
			for r in list(range(10)) :
				bdc( r&1, (r&2)>>1, (r&4)>>2, (r&8)>>3 )
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
print "All done"
