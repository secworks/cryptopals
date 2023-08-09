#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#=======================================================================
#
# CC_problem_2_1.py
# -----------------
# Python solution to problem 2 in set 1 of the Matasano
# Crypto Challenges.
#
#
# Problem description:
#
# Write a function that takes two equal-length buffers and produces
# their XOR sum.
# 
# The string:
# 
#  1c0111001f010100061a024b53535009181c
# 
# ... after hex decoding, when xor'd against:
# 
#  686974207468652062756c6c277320657965
# 
# ... should produce:
# 
#  746865206b696420646f6e277420706c6179
#
#
# (c) 2012 Secworks Sweden AB
# Joachim Strombergson
#
#=======================================================================

import CC_functions

#-------------------------------------------------------------------
# xorstring()
#
# Given two hex encoded strings returns the hex encoded string
# that represent the values in XORed together. 
#-------------------------------------------------------------------
def xorstring(string1, string2):
    assert len(string1) == len(string2), "Strings are not equal length."

    xorstring = ""
    values1 = CC_functions.string2val(string1)
    values2 = CC_functions.string2val(string2)
    
    for i in range(len(values1)):
        xorstring += '{:02x}'.format((values1[i] ^ values2[i]))
    
    return xorstring


#-------------------------------------------------------------------
# main()
#
# Run the functions to solve the problem with the given test case.
#-------------------------------------------------------------------
def main():
    instring1 = "1c0111001f010100061a024b53535009181c"
    instring2 = "686974207468652062756c6c277320657965"
    refstring = "746865206b696420646f6e277420706c6179"

    genstring = xorstring(instring1, instring2)

    print "CryptoChallenge Problem 2_1:"
    print "----------------------------"
    print "Input strings:"
    print instring1
    print instring2
    print ""
    print "Generated XOr string:"
    print genstring
    print ""

    if genstring != refstring:
        print "Error: Generated XOR string differ from expected reference string."
        print "Expected string:"
        print refstring

    else:
        print "Generated string is correct."


#-------------------------------------------------------------------
# __name__
# Python thingy to run as a stand alone if called.
#-------------------------------------------------------------------
if __name__ == '__main__':
    main()

#=======================================================================
# EOF CC_problem_2_1.py
#=======================================================================
