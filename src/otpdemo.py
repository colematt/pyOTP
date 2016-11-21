#!/usr/bin/env python3

"""
File: otp.py
Author: Matthew Cole, Anh Quach, Dan Townley,
Date: 11/20/16
"""
import time
import sys
import otp

"""
Utility functions
"""
def _header(mode="TOTP", digits=6):
	return  " ".join(["Timestamp".ljust(24), "Time Step".ljust(18), mode.ljust(digits), "Expired".ljust(10),\
					  "\n"+"-"*24,           "-"*18,                "-"*digits,         "-"*10])

def _expirebar(t, width=10, filltime=30):
	"""
	Print a timed expire bar of @param width '▩' characters.
	<t> is a number of seconds since the Unix epoch.
	The caller is responsible to add any ending whitespace
	characters needed after the final '▩'.
	"""

	#Calcuate the step time (time between each fill block)
	# and stop time (time when the bar is filled)
	start = t - (t % filltime) # (Unix Epoch) + (k)(filltime)
	step = filltime // width
	stop = start + filltime	   # (Unix Epoch) + (k+1)(filltime)

	#Initialy fill the bar, reflecting fraction expired at calltime
	intfill = ((t - start) // filltime) * width
	print(chr(9641)*(intfill),end="")

	# For each of (filltime / width) intervals,
	# print a fill block
	for t in range(start, stop, step):
		# Wait until the next time interval has passed
		while (int(time.time()) < t):
			pass

		# Print another fill block and flush
		print(chr(9641), end="")
		sys.stdout.flush()

if __name__ == "__main__":

	DIGITS = 6
	TIME = 30

	# Print the header
	print(_header())

	# Calculate first step
	now = int(time.time())
	next = now - (now % TIME) + TIME
	ts = otp.T(now, TIME)
	totp = otp.TOTP(otp.TOKEN,ts,DIGITS)


	# Continue generating TOTP passwords until halted by user
	while(True):

		# Print the next TOTP data
		print(time.asctime(time.localtime(now)), hex(ts).ljust(18), totp.ljust(DIGITS), sep=" ", end = " ")
		sys.stdout.flush()

		# Print the next expiration bar
		_expirebar(now, filltime=TIME)
		print("")
		sys.stdout.flush()

		# Step forward, recalculate T
		now = next
		next += TIME
		ts = otp.T(now, TIME)
		totp = otp.TOTP(otp.TOKEN,ts,DIGITS)
