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
import unittest
import dateutil.parser


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
	Raises ValueError for invalid or unknown string format, if the provided tzinfo is not in a valid format, or if an invalid date would be created. 
	Raises OverflowError if the parsed date exceeds the largest valid C integer on your system.
	"""

	# t is already usable (user probably passed int(time.time()) as argument)
	if type(t) == int:
		pass
	#time.time() provides current time as a floating point integer,
	#this can cause problems later
	elif type(t) == float:
		t = int(math.floor(t))

	#Down-cast struct_time types to an integer number of seconds
	elif type(t) == time.struct_time:
		t = time.mktime(t)

	# Otherwise, use dateutil.parser to attempt to convert as a string input,
	# then calculate seconds since the Unix epoch using datetime.timestamp()
	else:
		t = int(dateutil.parser.parse(str(t)).timestamp())
		
	# Calculate time steps using default floor function
	# and integer division
	return int(t // X)

def _HS(K,C,digest):
	"""
	Generate a 20 byte HMAC value. Unlike RFC 4226, we do not convert it to a 
	string representation since we use it as an intermediate value only.
	"""
	# Pad the secret to a multiple of block size (8)
	K = str(K)
	pad = len(K) % 8
	if pad != 0:
		K += '=' * (8 - pad)
	
	# Decode the secret to a bytes object
	K = base64.b32decode(K, casefold=True)

	# Convert the counter to a byte array
	ba = bytearray()
	while C != 0:
		ba.append(C & 0xFF)
		C >>= 8
	C = bytes(bytearray(reversed(ba)).rjust(8, b'\0'))

	# Initialize the HMAC hasher and digest the secret
	hasher = hmac.new(K,C,digest)
	return bytearray(hasher.digest())

	
def _DT(hs):
	"""
	Truncate a 20-byte HMAC value to a 4-byte object. Unlike RFC 4226, we
	do not convert it to a string representation since we use it as an
	intermediate value only.
	"""
	offset = hs[-1] & 0xf
	return ((hs[offset] & 0x7f) << 24 | (hs[offset + 1] & 0xff) << 16 | (hs[offset + 2] & 0xff) << 8 | (hs[offset + 3] & 0xff))


def HOTP(K,C,digit=6,digest=hashlib.sha1):
	"""
	Return the HOTP-value for base-32 representation Key <K>,
	Counter <C>, with <digits> width, and hashing mode <mode>.
	Return type is a string.
	"""
	#Process the selected digest
	if type(digest) == str:
		try:
			digest = getattr(hashlib,digest.lower())
		except AttributeError:
			print("Digest mode \'%s\' not one of: %s" % (str(digest), str(hashlib.algorithms_guaranteed)))
			raise
		
	# Digest count with the key, and truncate the result
	sbits = _DT(_HS(K,C,digest))
	
	# Convert the digested/truncated bits into an HOTP string value
	return str(sbits % 10 ** digit).rjust(digit, '0')

	
def TOTP(K,C=None,digit=6,digest=hashlib.sha1):
	"""
	Return the TOTP-value for Key <K>, Time Step as Counter <C>,
	with <digits> width, and hash digest <mode>. Return type is a string.
	"""
	if not C:
		C = T()
	return HOTP(K,C,digit=digit,digest=digest)

class TestHOTP(unittest.TestCase):
	"""
	Class implementing the RFC 4226 Appendix D tests.
	"""
	
	Secret = "12345678901234567890"
	
	IntermediateValues = [0xcc93cf18508d94934c64b65d8ba7667fb7cde4b0,
							0x75a48a19d4cbe100644e8ac1397eea747a2d33ab,
							0x0bacb7fa082fef30782211938bc1c5e70416ff44,
							0x66c28227d03a2d5529262ff016a1e6ef76557ece,
							0xa904c900a64b35909874b33e61c5938a8e15ed1c,
							0xa37e783d7b7233c083d4f62926c7a25f238d0316,
							0xbc9cd28561042c83f219324d3c607256c03272ae,
							0xa4fb960c0bc06e1eabb804e5b397cdc4b45596fa,
							0x1b3c89f65e6c9e883012052823443f048b4332db,
							0x1637409809a679dc698207310c8c7fc07290d9e5]
	TruncatedValues = [0x4c93cf18,
						0x41397eea,
						0x82fef30,
						0x66ef7655,
						0x61c5938a,
						0x33c083d4,
						0x7256c032,
						0x4e5b397,
						0x2823443f,
						0x2679dc69]
	HOTPValues = ["755224",
					"287082",
					"359152",
					"969429",
					"338314",
					"254676",
					"287922",
					"162583",
					"399871",
					"520489"]
					
class TestTOTP(unittest.TestCase):
	"""
	Class implementing the RFC 6238 Appendix B tests.
	"""
	
	Secret = "12345678901234567890"
	X = 30
	T0 = 0
	
	UTCTimes = ["1970-01-01 00:00:59 UTC",
				"2005-03-18 01:58:29 UTC",
				"2005-03-18 01:58:31 UTC",
				"2009-02-13 23:31:30 UTC",
				"2033-05-18 03:33:20 UTC",
				"2603-10-11 11:33:20 UTC"]
	TValues = [0x0000000000000001,
				0x00000000023523EC,
				0x00000000023523ED,
				0x000000000273EF07,
				0x0000000003F940AA,
				0x0000000027BC86AA]
	TOTP_SHA1Values = ["94287082",
						"07081804",
						"14050471",
						"89005924",
						"69279037",
						"65353130"]
	TOTP_SHA256Values = ["46119246",
							"68084774",
							"67062674",
							"91819424",
							"90698825",
							"77737706"]
	TOTP_SHA512Values = ["90693936",
							"25091201",
							"99943326",
							"93441116",
							"38618901",
							"47863826"]