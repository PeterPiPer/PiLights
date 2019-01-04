#!/usr/bin/python

# Playtime with DS1307 realtime clock and the I2C interface
# Need to create get & set functions (once I've found my way around).

import smbus
# todo said thar threading was easier, but for what i want this
#doesn't seem like a prob, investigate docs
import thread
import time
import sys


# DS1307 i2c address from manufacturer datasheet
CLOCK_ADDR = 0b1101000
# Time keeper register addresses
SEC_ADDR = 0x00
MIN_ADDR = 0x01
HRS_ADDR = 0x02
DAY_ADDR = 0x03
DAT_ADDR = 0x04
MTH_ADDR = 0x05
YER_ADDR = 0x06


# todo add proper documentation
# todo decide what to do with 12/24 hr fmt
class RealTimeClock:
	def __init__(self, time_24_hour=True, channel=0):
		self.__seconds = 0;
		self.__minutes = 0;
		self.__hours = 0;
		self.__day = 0;
		self.__date = 0;
		self.__month = 0;
		self.__year = 0;
		self.__time24_hour = True;
		self.__lock = thread.allocate_lock()
		try:
			self.__bus = smbus.SMBus(channel)
		except IOError:
			raise ValueError("I2C channel %d not found" % channel)


	def clock_run(self):
		thread.start_new_thread(self.__read_clock,())

	# Don't anticipate using as i want the clock to run cnostantly,
	# but there for completeness
	def stop_clock(self):
		self.__lock.acquire()
		__bus.write_byte_data(CLOCK_ADDR, 0, 0b10000000)
		#todo  threading ? stop?
		self.__lock.release()


	# Time must alwasy be presented as arg in 24hr format
	def set_time(	self,
			year=2019,
			month=1,
			date=1,
			hours=0,
			minutes=0,
			seconds=0):

		seconds_ten = seconds / 10
		seconds_unit = seconds % 10
		# NB I'll always unset the 7th bit which is CH (Clock Halt)
		# CH=1 clock halt, CH=0 run, as I assume we want the clock 
		# running if we're setting the time. 
		sec_set_byte = 0b00000000 | (seconds_ten<<4) | seconds_unit

		minutes_ten = minutes / 10
		minutes_unit = minutes % 10
		min_set_byte = 0b00000000 | (minutes_ten<<4) | minutes_unit

		if self.__time24_hour == True:
			hour_fmt = 0b00000000
			if hours > 19:
				hours_ten = 0b011
			elif hours > 9:
				hours_ten = 0b001
			else:
				hours_ten = 0b0
				
			hours_unit = hours % 10
		else:
			#todo  work out how bit 4&5 of hours is used 4sure.
			# bit6 high for 12 hr mode
			hour_fmt = 0b01000000
			if hours >= 12:
				hours -= 12
				#Set bit 5 high for PM
				hour_fmt |= 0b00100000
				hours_ten = hours/10
			else:
				hours_ten = hours/10
			hours_unit = hours % 10
				
		hour_set_byte = hour_fmt | (hours_ten<<4) | hours_unit

		# will not set the day as not using on my clock
		# for completeness could get from date functions
		# todo - maybe come back to this later after first pass works
		day_set_byte = 0;

		date_ten = date / 10
		date_unit = date % 10
		date_set_byte = (date_ten<<4) | date_unit

		mnth_ten = month / 10
		mnth_unit = month % 10
		mnth_set_byte = (mnth_ten<<4) | mnth_unit

		year_ten = year / 10
		year_unit = year % 10
		year_set_byte = (year_ten<<4) | year_unit

		self.__lock.acquire()
		
		# Write to DS1307 over I2C
		self.__bus.write_byte_data(CLOCK_ADDR, SEC_ADDR, sec_set_byte)
		self.__bus.write_byte_data(CLOCK_ADDR, MIN_ADDR, min_set_byte)
		self.__bus.write_byte_data(CLOCK_ADDR, HRS_ADDR, hour_set_byte)
		self.__bus.write_byte_data(CLOCK_ADDR, DAY_ADDR, day_set_byte)
		self.__bus.write_byte_data(CLOCK_ADDR, DAT_ADDR, date_set_byte)
		self.__bus.write_byte_data(CLOCK_ADDR, MTH_ADDR, mnth_set_byte)
		self.__bus.write_byte_data(CLOCK_ADDR, YER_ADDR, year_set_byte)

		# Set internal representation
		self.__seconds = seconds;
		self.__minutes = minutes;
		self.__hours = hours;
		self.__date = date;
		self.__month = month;
		self.__year = year;

		self.__lock.release()

	# Runs in internal thread
	# TODO consider cleanup code & clean exit or thread stop
	def __read_clock(self):
		try:
			#todo may want some exception handling in here...
			while True:
				self.__lock.acquire()

				secs = self.__bus.read_byte_data(CLOCK_ADDR,
								SEC_ADDR)
				mins = self.__bus.read_byte_data(CLOCK_ADDR, 
								MIN_ADDR)
				hours = self.__bus.read_byte_data(CLOCK_ADDR, 
								HRS_ADDR)
				day = self.__bus.read_byte_data(CLOCK_ADDR, 
								DAY_ADDR)
				date = self.__bus.read_byte_data(CLOCK_ADDR, 
								DAT_ADDR)
				month = self.__bus.read_byte_data(CLOCK_ADDR, 
								MTH_ADDR)
				year = self.__bus.read_byte_data(CLOCK_ADDR, 
								YER_ADDR)

				# Extract real values from register structure
				self.__seconds = (secs & 0b00001111) + \
						((secs>>4)&0b0111)*10
				self.__minutes = (mins & 0b00001111) + \
						((mins>>4)&0b0111)*10
				#todo maybe i should use the value i read for fmt
				if self.__time24_hour == True:
					self.__hours = (hours & 0b00001111) + \
						((hours>>4)&0b0011)*10
				else:
					self.__hours = (hours & 0b00001111)+ \
						((hours>>4)&0b0011)*10

				self.__day = 0  
				self.__date = (date & 0b00001111)+ \
						((date>>4)&0b0011)*10
				self.__month = (month & 0b00001111)+ \
						((month>>4)&0b0001)*10
				self.__year = (year & 0b00001111)+ \
						((year>>4)&0b1111)*10
				self.__lock.release()

				time.sleep(0.25)
		except Exception:
			pass
	
	def get_time(self):
		self.__lock.acquire()
		# NB will use time as tuple of 9 integers
		# As I don't care about the day julian day or DST at the moment
		# will just set these to zero
		timet = (	2000+self.__year,
				self.__month,
				self.__date,
				self.__hours,
				self.__minutes,
				self.__seconds,
				0, 0, 0)
		self.__lock.release()
		
		return timet


def read_time(bus):
	sec = bus.read_byte_data(CLOCK_ADDR, 0)
	min = bus.read_byte_data(CLOCK_ADDR, 1)
	hour = bus.read_byte_data(CLOCK_ADDR, 2)
	day = bus.read_byte_data(CLOCK_ADDR, 3)
	date = bus.read_byte_data(CLOCK_ADDR, 4)
	month = bus.read_byte_data(CLOCK_ADDR, 5)
	year = bus.read_byte_data(CLOCK_ADDR, 6)
	
	print( bin(year), "|", bin(month), "|", bin(date), "|", bin(day), " ", bin(hour), ":", bin(min), ":", bin(sec) )




if __name__ == "__main__":
	print "Hello testing it out...", sys.argv[1]
	t1=sys.argv[1]
	if t1 == "tell":
		rtc = RealTimeClock()
		rtc.clock_run()

		try:
			while True:
				time.sleep(15)
				st = time.asctime(rtc.get_time())
				print("time is %s" % st )
		except KeyboardInterrupt:
			pass

	elif t1 == "set":
		rtc = RealTimeClock()
		rtc.clock_run()
		rtc.set_time( 19, 1, 4, 1, 15, 30)
		time.sleep(2)

		st = time.asctime(rtc.get_time())
		print("time is %s" % st )
	else:
		clock_bus = smbus.SMBus(0)

		while True:
			read_time(clock_bus)
			time.sleep(5)


