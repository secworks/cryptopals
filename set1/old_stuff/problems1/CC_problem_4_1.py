#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#=======================================================================
#
# CC-problem_4_1.py
# -----------------
# Python solution to problem 4 in set 1 of the Matasano
# Crypto Challenges.
#
#
# Problem description:
# Detect single-character XOR
# 
# One of the 60-character strings at:
# 
#   https://gist.github.com/3132713
# 
# has been encrypted by single-character XOR. Find it.
# (Your code from problem 3 should help.)
#
# 
# Notes: The gistfile.txt is 19945 Bytes long, which does not
# divide evenly with 60, 128 or 30.
#
#
# (c) 2012 Secworks Sweden AB
# Joachim Strombergson
#
#=======================================================================

import CC_functions
import math


#-------------------------------------------------------------------
# main()
#
# Run the functions to solve the problem with the given test case.
#-------------------------------------------------------------------
def main():
    print "CC Problem 4_1."
    print ""

    eng_freq = {'a':0.08167, 'b':0.01492, 'c':0.02782, 'd':0.04253,
                'e':0.12702, 'f':0.02228, 'g':0.02015, 'h':0.06094,	
                'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025,
                'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929,
                'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056,
                'u':0.02758, 'v':0.00978, 'w':0.02360, 'x':0.00150,	
                'y':0.01974, 'z':0.00074}

    eng_bigrams = ['th', 'he', 'an', 're', 'er', 'in', 'on', 'at',
                   'nd', 'st', 'es', 'en', 'of', 'te', 'ed', 'or',
                   'ti', 'hi', 'as', 'to', 'll', 'ee', 'ss', 'oo',
                   'tt', 'ff', 'rr', 'nn', 'pp', 'cc']

    eng_trigrams = ['the', 'and', 'tha', 'ent', 'ing', 'ion',
                    'tio', 'for', 'nde', 'has', 'nce', 'edt',
                    'tis', 'oft', 'sth', 'men']

    eng_lang = (eng_freq, eng_bigrams, eng_trigrams)


    encoded_strings = []
    with open("./data/data_CC_3_1.txt", 'r') as f:
        for line in f.readlines():
            encoded_strings.append(CC_functions.hexstring2string(line.strip()))
    print encoded_strings

    for string in encoded_strings:
        xor_value = CC_functions.findxorval(string, eng_lang)
        print "The string was XOR encoded using byte value 0x%02x" % xor_value
        print "Decoded string:"
        print CC_functions.xorstring(string, chr(xor_value))
        
    
#-------------------------------------------------------------------
# __name__
# Python thingy to run as a stand alone if called.
#-------------------------------------------------------------------
if __name__ == '__main__':
    main()

#=======================================================================
# EOF CC_problem_4_1.py
#=======================================================================
