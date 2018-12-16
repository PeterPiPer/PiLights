#!/usr/bin/python

import time as time
import RPi.GPIO as GPIO

# experiment with the output thatseem to be behaving oddly



# GPIO-14+15: set for output, got warining that in use (led was lit from start).
# Doc says UART: TXD 14
# Doc says UART: RXD 15
# Some google refs about being set up for llserial console access & that
# this needs to be disabled in pie config before I can use.
# can set for output though

# GPIO 18 all good for output as expected
# GPIO 24 all good for out put as expected - Says in use, ignoring & do anyway
# GPIO 25 all good for out put as expected - Says in use, ignoring & do anyway
# GPIO 7 all good for out put as expected

# GPIO 23 - All good (was previously shorted on board)
# GPIO  8 - All good (was previously shorted on board)
# GPIO  9 - All good (was previously shorted on board)
#-------

# GPIO 11 all good for out put as expected
# GPIO 10 all good for out put as expected
# GPIO 22 all good for out put as expected
# GPIO 17 all good for out put as expected

# GPIO 0 - on faintly from start
# 	GPIO 0 all good for output as expected
# GPIO 4 all good for out put as exprected
# GPIO 1 - on faintly from start
# 	GPIO 1 all good for output as expected

GPIO.setmode (GPIO.BCM)

GPIO.cleanup()

gpioTest = 18

GPIO.setup (gpioTest, GPIO.OUT)

for x in list(range(5)):
	GPIO.output (gpioTest, True)
	time.sleep (1)
	GPIO.output (gpioTest, False)
	time.sleep (1)

GPIO.cleanup()
