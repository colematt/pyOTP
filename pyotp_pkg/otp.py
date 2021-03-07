#!/usr/bin/env python3

"""
File: otp.py
Author: Matthew Cole, Anh Quach, Dan Townley
Date: 11/20/16
"""
import math
import time
import hashlib
import hmac
import base64

"""
Constants specified by RFC 6238
"""

DIGESTS = {"sha1":hashlib.sha1, "sha256":hashlib.sha256, "sha512":hashlib.sha512}


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


def T(t=time.time(), X=30):
	"""
	Return number of time steps between T0 (the Unix epoch) and t.
	"""
	#time.time() provides a time as a floating point integer,
	#this can cause problems later
	if type(t) == float:
		t = int(math.floor(t))

	#Down-cast struct_time types to an integer
	#number of seconds, if needed
	if type(t) == time.struct_time:
		t = time.mktime(t)

	# Calculate time steps using default floor function
	# and integer division
	return int(t // X)

def HOTP(K,C,digit=6, digest=hashlib.sha1):
	"""
	Return the HOTP-value for base-32 representation Key <K>,
	Counter <C>, with <digits> width, and hashing mode <mode>.
	Return type is a string.
	"""
	#Sanity check on digest mode
	try:
		if type(digest) == str:
			digest = DIGESTS[digest]
	except ValueError:
		print("Digest mode (%s) not one of: %s" % (str(digest), str(hashlib.algorithms_guaranteed)))

	# Pad the secret; it must have a length of
	# a multiple of block size (8)
	# Then decode it to a bytes object
	K = str(K)
	pad = len(K) % 8
	if pad != 0:
		K += '=' * (8 - pad)
	K = base64.b32decode(K, casefold=True)

	# Convert the counter to a byte array
	ba = bytearray()
	while C != 0:
		ba.append(C & 0xFF)
		C >>= 8
	C = bytes(bytearray(reversed(ba)).rjust(8, b'\0'))

	# Initialize the HMAC-SHA hasher
	hasher = hmac.new(K,C, digest)
	hm = bytearray(hasher.digest())

	# Truncate as specified in RFC
	offset = hm[-1] & 0xf
	code = ((hm[offset] & 0x7f) << 24 | (hm[offset + 1] & 0xff) << 16 | (hm[offset + 2] & 0xff) << 8 | (hm[offset + 3] & 0xff))
	str_code = str(code % 10 ** digit)

	# Left pad with zeros
	str_code = str_code.rjust(digit, '0')

	return str_code

def TOTP(K,C=None,digit=6,digest=hashlib.sha1):
	"""
	Return the TOTP-value for Key <K>, Time Step as Counter <C>,
	with <digits> width, and hash digest <mode>. Return type is a string.
	"""
	if not C:
		C = T()
	return HOTP(K,C,digit=digit,digest=digest)

if __name__ == "__main__":

    """
    This code is used for the test target in the Makefile.
    It's a series of assertions and output messages that aren't particularly
    useful to the end-user, but they are specified by the RFCs.
    """
