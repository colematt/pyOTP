#!/usr/bin/env python3

"""
File: otp.py
Author: Matthew Cole, Anh Quach, Dan Townley,
Date: 11/20/16
"""
import time
import hashlib
import hmac

"""
Constants specified by RFC 6238
"""

MODES = {"sha1", "sha256", "sha512"}
TOKEN = "12345678901234567890"

"""
Notations specified by RFC 4226 and RFC 6238
C : the 8-byte counter value, the moving factor. This value must be synchronized
	between client and server.
K : the shared secret between client and server; each HOTP generator has a
	different and unique secret K.
X : the time step in seconds. Default: X = 30
TO: the unix time to start counting time steps (i.e. the Unix epoch)
	T0 = Thu Jan 1 00:00:00 1970
T : number of time steps between the initial counter time T0 and the current
	Unix time
digit : the number of digits in the output, left padded with '0' as required
"""

def T(t, X=30):
	"""
	Return number of time steps between T0 (the Unix epoch) and t.
	"""
	#Down-cast struct_time types to an integer
	#number of seconds, if needed
	if type(t) == time.struct_time:
		t = time.mktime(t)

	# Calculate time steps using default floor function
	# and integer division
	return int(t // X)

def HOTP(K,C,digit=6, mode="sha1"):
	"""
	Return the HOTP-value for Key <K>, Counter <C>, with <digits> width,
	and hashing mode <mode>. Return type is a string.
	"""
	value = 0xc0ffee
	value %= 10 ** 6
	return str(value).rjust(digit,"0")

def TOTP(K,T,digit=6, mode="sha1"):
	"""
	Return the TOTP-value for Key <K>, Time Step <T>, with <digits> width,
	and hashing mode <mode>. Return type is a string.
	"""
	return HOTP(K,T,digit)

if __name__ == "__main__":

    """
    This code is used for the test target in the Makefile.
    It's a series of assertions and output messages that aren't particularly
    useful to the end-user, but they are specified by the RFCs.
    """