#!/usr/bin/python

import time
import RPi.GPIO as GPIO

# Cos I can never remember which pin is which, and I keep loosing the pinout
# sheet for older pi, lets me double check by trail & error

def gpioFlash(pin) :
	GPIO.output (pin, True)
	print "GPIO ", pin
	time.sleep (3)
	GPIO.output (pin, False)

GPIO.setmode (GPIO.BCM)
GPIO.setup (1, GPIO.OUT)
GPIO.setup (4, GPIO.OUT)
GPIO.setup (0, GPIO.OUT)
GPIO.setup (17, GPIO.OUT)
GPIO.setup (22, GPIO.OUT)
GPIO.setup (10, GPIO.OUT)
GPIO.setup (11, GPIO.OUT)
GPIO.setup (21, GPIO.OUT)
GPIO.setup (9, GPIO.OUT)
GPIO.setup (8, GPIO.OUT)
GPIO.setup (23, GPIO.OUT)
GPIO.setup (7, GPIO.OUT)
GPIO.setup (25, GPIO.OUT)
GPIO.setup (24, GPIO.OUT)
GPIO.setup (18, GPIO.OUT)
GPIO.setup (15, GPIO.OUT)
GPIO.setup (14, GPIO.OUT)


try: 
	while True:
		gpioFlash(1)
		gpioFlash(4)
		gpioFlash(0)
		gpioFlash(17)
		gpioFlash(22)
		gpioFlash(10)
		gpioFlash(11)
		gpioFlash(21)
		gpioFlash(9)
		gpioFlash(8)
		gpioFlash(23) # or 23 or 2?
		gpioFlash(7)
		gpioFlash(25)
		gpioFlash(24)
		gpioFlash(18)
		gpioFlash(15)
		gpioFlash(14)
except KeyboardInterrupt:
	GPIO.cleanup()
except:
	print "Error occurred."

