#!/usr/bin/python

import time as time
import RPi.GPIO as GPIO

# Read a loadcell 0-5kg range - uses HX711 module
# tech specs & connection details in LoadCell.md

global GPIO_DT
global GPIO_SCK
GPIO_DT = 7
GPIO_SCK = 23

def bitDump(word, debug=False) :
        buf = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(24) :
                buf[23-i] = (word &2**i)>>i
        if (debug) :
                print "Word in: ", word, "bits: ", buf
        return buf
# End bitDump


GPIO.setmode (GPIO.BCM)

GPIO.setup (GPIO_SCK, GPIO.OUT)
GPIO.setup (GPIO_DT, GPIO.IN)

GPIO.output(GPIO_SCK, GPIO.LOW )

try:
	while True:
		time.sleep(2)
		if (GPIO.input(GPIO_DT) == GPIO.LOW ) :
			weight = 0
			print "DT Low data ready to retrieve"
			for i in range(25) :
				GPIO.output(GPIO_SCK, GPIO.HIGH )
				time.sleep(0.001)
				inp =  GPIO.input(GPIO_DT)
				print "DT value is ", inp
				weight = (weight<<1) | inp
				GPIO.output(GPIO_SCK, GPIO.LOW )
				time.sleep(0.001)
			print "Weight is: ", weight, " In bin: ", bitDump(weight)
		else :
			print "DT Hih not ready to read"

except KeyboardInterrupt:
	GPIO.cleanup()
#end try

