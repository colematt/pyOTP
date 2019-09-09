#!/usr/bin/env python3

"""
File: otp.py
Author: Matthew Cole, Anh Quach, Dan Townley,
Date: 11/20/16
"""
import time
import sys
import otp
import provision
import argparse
import hashlib

try:
	from PIL import Image
	import zbarlight
except(ImportError):
	print("Prerequisites not met! pyOTP requires zbarlight.", file=sys.stderr)
	print("See https://github.com/Polyconseil/zbarlight for more information.", file=sys.stderr)
	raise

def _printURI(uri):
	"""
	Read a URI from a .png image file. Return its contents as a pretty string.
	"""
	### QR Code reading using zbarlite
	try:
		with open(uri, 'rb') as image_file:
			image = Image.open(image_file)
			image.load()
		codes = zbarlight.scan_codes('qrcode', image)
	except(IOError):
		print("Cannot open %s" % uri, file=sys.stderr)
		raise

	#If there's a readable barcode, deprovision it
	if len(codes) == 1:
		type,name,secret,issuer,algorithm,digits,period = otp.deprovision(codes[0].decode())
	else:
		print("Found %i valid QR Codes in %s. Cannot decode!" % (len(codes), uri), file=sys.stderr)
		raise IOError

	#Log URI contents
	print("Type:", type)
	print("Name:", name)
	print("Secret:", secret)
	print("Issuer:", issuer)
	print("Algorithm:", algorithm)
	print("Digits:", digits)
	print("Period:", period)

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

	# Argument parsing
	parser = argparse.ArgumentParser(description='demonstrate the TOTP algorithm')
	parser.add_argument('--displayuri', help='display the contents of the URI', action="store_true")
	parser.add_argument('qrfile', help="path to the shared secret key QR Code .png file")
	args = parser.parse_args()

	### QR Code reading using zbarlite
	try:
		with open(args.qrfile, 'rb') as image_file:
			image = Image.open(image_file)
			image.load()
		codes = zbarlight.scan_codes('qrcode', image)
	except(IOError):
		print("Cannot open %s" % args.qrfile, file=sys.stderr)
		exit(0)

	#If there's a readable barcode, deprovision it
	if len(codes) == 1:
		_,_,secret,_,mode,digit,x = provision.deprovision(codes[0].decode())
		mode = getattr(hashlib,mode.lower())

	else:
		print("Found %i valid QR Codes in %s. Cannot decode!" % (len(codes), args.qrfile), file=sys.stderr)
		exit(0)

	# Print the URI read
	if args.displayuri:
		_printURI(args.qrfile)

	# Print the header
	print(_header())

	# Calculate first step
	now = int(time.time())
	next = now - (now % x) + x
	ts = otp.T(now, x)
	totp = otp.TOTP(secret,ts,digit=digit, digest=mode)

	# Continue generating TOTP passwords until halted by user
	while(True):

		# Print the next TOTP data
		print(time.asctime(time.localtime(now)), hex(ts).ljust(18), totp.ljust(digit), sep=" ", end = " ")
		sys.stdout.flush()

		# Print the next expiration bar
		try:
			_expirebar(now, filltime=x)
		except (KeyboardInterrupt, SystemExit):
			print("\nExiting OTP Demo...")
			sys.exit(0)
		finally:
			print("")
			sys.stdout.flush()
			
		# Step forward, recalculate T
		now = next
		next += x
		ts = otp.T(now, x)
		totp = otp.TOTP(secret,ts,digit=digit, digest=mode)
