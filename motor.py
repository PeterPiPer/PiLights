#!/usr/bin/python

import time as time
import RPi.GPIO as GPIO

# Drive a stepper motor 
global GPIO_blue
global GPIO_pink
global GPIO_yellow
global GPIO_orange
GPIO_blue = 11
GPIO_pink = 10
GPIO_yellow = 22
GPIO_orange = 17

def stepMotor(blue, pink, yellow, orange, zzz):
	GPIO.output (GPIO_blue, blue)
	GPIO.output (GPIO_pink, pink )
	GPIO.output (GPIO_yellow, yellow)
	GPIO.output (GPIO_orange, orange)
	time.sleep(zzz)
	return

GPIO.setmode (GPIO.BCM)

GPIO.cleanup()

GPIO.setup (GPIO_blue, GPIO.OUT)
GPIO.setup (GPIO_pink, GPIO.OUT )
GPIO.setup (GPIO_yellow, GPIO.OUT)
GPIO.setup (GPIO_orange, GPIO.OUT)

stepInterval = 0.01
#stepInterval = 0.0001-0.0005 interval too short just hums
#stepInterval = 0.0007 jerky, stop & start
#stepInterval = 0.0008 turns freely at ~14.8 rpm

# Motor28BYJ-48
# 8 steps per turn: geared 1:64, 8*64 steps for a single turm
# however i seem to need 8*512? worry about this later, spec said 4096 steps
'''
for r in list(range(10)) :
	for x in list(range(512)) :
		# face on anit clockwise
		stepMotor(0, 0, 0, 1, stepInterval)
		stepMotor(0, 0, 1, 1, stepInterval)
		stepMotor(0, 0, 1, 0, stepInterval)
		stepMotor(0, 1, 1, 0, stepInterval)
		stepMotor(0, 1, 0, 0, stepInterval)
		stepMotor(1, 1, 0, 0, stepInterval)
		stepMotor(1, 0, 0, 0, stepInterval)
		stepMotor(1, 0, 0, 1, stepInterval)
'''
# Clockwise
for x in list(range(512)) :
	# face on anit clockwise
	stepMotor(1, 0, 0, 1, stepInterval)
	stepMotor(1, 0, 0, 0, stepInterval)
	stepMotor(1, 1, 0, 0, stepInterval)
	stepMotor(0, 1, 0, 0, stepInterval)
	stepMotor(0, 1, 1, 0, stepInterval)
	stepMotor(0, 0, 1, 0, stepInterval)
	stepMotor(0, 0, 1, 1, stepInterval)
	stepMotor(0, 0, 0, 1, stepInterval)


GPIO.cleanup()
