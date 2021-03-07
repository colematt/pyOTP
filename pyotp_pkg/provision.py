#!/usr/bin/env python3
# provision.py

import urllib.parse
import sys
import typing
from icecream import ic

try:
	from PIL import Image
	import zbarlight
except ImportError as ie:
	print("PyOTP prerequisite not met: %s" % ie.name)
	print("See https://github.com/colematt/pyOTP/blob/master/README.md#installation for more information.", file=sys.stderr)
	raise(ie)

def scan(path):
	try:
		with open(path, 'rb') as ifile:
			image = Image.open(ifile)
			image.load()
			codes = [zbarlight.scan_codes(symbology,image) for symbology in zbarlight.Symbologies.keys()]
			codes = list(filter(lambda c: bool(c), codes))
			if len(codes) > 1:
				raise(ValueError("Multiple symbologies detected in %s" % path))
			if len(codes[0]) > 1:
				raise(ValueError("Multiple URIs detected in %s" % path))
			else:
				return(codes.pop().pop())
	except IOError:
		raise IOError("Cannot open %s" % path)

def provision(source):
	pass

def main():
	print(dir(zbarlight))
	source = scan('../docs/test.png')
	# result = parse(source)

	print(urllib.parse.urlparse(b''))
	


if __name__ == '__main__':
	main()

# def provision(tup):
# 	"""
# 	Convert a type URI 9-tuple into a well-formed URI string
# 	"""
# 	#Partitioning
# 	type, name, secret, issuer, algorithm, digits, period = tup

# 	#Assembling
# 	uri = "otpauth://" + type + "/" + issuer + ":" + name + "?" +\
# 	"secret=" + secret +\
# 	"&issuer=" + issuer +\
# 	"&algorithm=" + algorithm.upper() +\
# 	"&digits=" + str(digits) +\
# 	"&period=" + str(period)

# 	return uri

# def deprovision(uri):
# 	"""
# 	Convert a URI string into a typed URI 9-tuple
# 	"""

# 	#Partitioning
# 	_,_,uri = uri.partition("://")
# 	type,_,uri = uri.partition("/")
# 	_,_,uri = uri.partition(":")
# 	name,_,uri = uri.partition("?")
# 	secret,issuer,algorithm,digits,period = uri.split("&")

# 	#Parsing
# 	secret = secret.split("=")[1]
# 	issuer = issuer.split("=")[1]
# 	algorithm = algorithm.split("=")[1].lower()
# 	digits = int(digits.split("=")[1])
# 	period = int(period.split("=")[1])
# 	tup = (type, name, secret, issuer, algorithm, digits, period)

# 	return tup