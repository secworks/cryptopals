#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#=======================================================================
#
# CC_problem_1_1.py
# -----------------
# Python solution to problem 1 in set 1 of the Matasano
# Crypto Challenges.
#
#
# Problem description:
#
# Convert hex to base64 and back.
# 
# The string:
# 
#   '49276d206b696c6c696e6720796f757220627261696e206\
#    c696b65206120706f69736f6e6f7573206d757368726f6f6d'
# 
# should produce:
# 
#   SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
# 
# Now use this code everywhere for the rest of the exercises.
# Here's a simple rule of thumb:
# 
# Always operate on raw bytes, never on encoded strings.
# Only use hex and base64 for pretty-printing.
#
#
# (c) 2012 Secworks Sweden AB
# Joachim Strombergson
#
#=======================================================================

#-------------------------------------------------------------------
# string2val()
#
# Given a string representing a sequence of 8-bit hexadecimal
# values the function returns an array with the corresponding
# values.
#-------------------------------------------------------------------
def string2val(hexstring):
    return [ord(c) for c in hexstring.decode('hex')]
    

#-------------------------------------------------------------------
# hex2base64()
#
# Given a string representing a sequence of 8-bit hexadecimal
# values the function returns the Base64 encoded representation
# of the values.
#
# Note: The current implementation does not implement
#       the padding needed for strings that does not contain
#       an even number of triplet values.
#-------------------------------------------------------------------
def hex2base64(hexstring):
    base64_table = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                    'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                    'w', 'x', 'y', 'z', '0', '1', '2', '3',
                    '4', '5', '6', '7', '8', '9', '+', '/']
    bin64 = ""
    tmpval = 0
    state = 0
    
    # Convert pairs of chars in the string to an array
    # with to the corresponding values.
    hexvaluelist = string2val(hexstring)

    # Loop over the hex values with a simple FSM generating
    # four Base64 characters for every three values.
    for val in hexvaluelist:
        if (state == 0):
            bin64 += base64_table[(val & 0xfc) >> 2]
            tmpval = (val & 0x03) << 4
            state = 1

        elif (state == 1):
            bin64 += base64_table[(tmpval + ((val & 0xf0) >> 4))]
            tmpval = (val & 0x0f) << 2
            state = 2

        else:
            tmp = (tmpval + ((val & 0xc0) >> 6))
            bin64 += base64_table[tmp]
            bin64 += base64_table[(val & 0x3f)]
            state = 0

    return bin64


#-------------------------------------------------------------------
# main()
#
# Run the functions to solve the problem with the given test case.
#-------------------------------------------------------------------
def main():
    instring = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    refstring = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    genstring = hex2base64(instring)

    print "CryptoChallenge Problem 1_1:"
    print "----------------------------"
    print "Input string:"
    print instring
    print ""
    print "Generated Base64 string:"
    print genstring
    print ""

    if genstring != refstring:
        print "Error: Generated Base64 differ from expected reference string."
    else:
        print "Generated string is correct."
    

#-------------------------------------------------------------------
# __name__
# Python thingy to run as a stand alone if called.
#-------------------------------------------------------------------
if __name__ == '__main__':
    main()

#=======================================================================
# EOF CC_problem_1_1.py
#=======================================================================
