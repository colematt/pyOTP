#!/usr/bin/python3

"""
File: provision.py
Author: Matthew Cole 
Date: 9/5/19
"""

def provision(tup):
    """
    Convert a type URI 9-tuple into a well-formed URI string
    """
    #Partitioning
    type, name, secret, issuer, algorithm, digits, period = tup

    #Assembling
    uri = "otpauth://" + type + "/" + issuer + ":" + name + "?" +\
    "secret=" + secret +\
    "&issuer=" + issuer +\
    "&algorithm=" + algorithm.upper() +\
    "&digits=" + str(digits) +\
    "&period=" + str(period)

    return uri

def deprovision(uri):
    """
    Convert a URI string into a typed URI 9-tuple
    """

    #Partitioning
    _,_,uri = uri.partition("://")
    type,_,uri = uri.partition("/")
    _,_,uri = uri.partition(":")
    name,_,uri = uri.partition("?")
    secret,issuer,algorithm,digits,period = uri.split("&")

    #Parsing
    secret = secret.split("=")[1]
    issuer = issuer.split("=")[1]
    algorithm = algorithm.split("=")[1].lower()
    digits = int(digits.split("=")[1])
    period = int(period.split("=")[1])
    tup = (type, name, secret, issuer, algorithm, digits, period)

    return tup
