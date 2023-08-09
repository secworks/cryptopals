#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#=======================================================================
#
# CC-functions.py
# ---------------
# Python functions developed as part of the Matasano Crypto Challenges.
# The functions are used by the problem solutions.
#
#
# (c) 2012 Secworks Sweden AB
# Joachim Strombergson
#
#=======================================================================

import math

#-------------------------------------------------------------------
# num_substrings()
#
# Given a string and a list of substrings returns the total number
# of substrings in the string.
#-------------------------------------------------------------------
def num_substrings(string, substrings):
    num = 0
    for ch in substrings:
        num += string.count(ch.lower())
    return num


#-------------------------------------------------------------------
# match_string_language()
#
# Support function to create a dictionary for a given string. The
# letters in the string is matched with the alphabet represented
# as keys in a dictionary. For each letter their frequency in the
# string is calculated. All letters not in the alphabet is
# accumulated into a separate key-value.
#-------------------------------------------------------------------
def match_string_language(string, language):
    (alphabet, bigrams, trigrams) = language

    my_db = {}
    my_db['length'] = len(string)
    my_db['not_in_alphabet'] = 0

    for c in alphabet:
        my_db[c] = 0
        
    # Scan string and update the db.
    for c in string:
        if c in alphabet:
            my_db[c] += 1
        else:
            my_db[c] = 0
            my_db['not_in_alphabet'] += 1

    # Match the string against bigrams and trigrams.
    my_db['bigrams'] = num_substrings(string, bigrams)
    my_db['trigrams'] = num_substrings(string, trigrams)

    # Here we do the string matching operation. Based on
    # number of trigrams, bigrams, frequency and amount
    # of characters not in the alphabet we create a match value.
    # The weight given to the different pointers have been
    # choosen rather non-scientifically. But the results seems
    # to give a rather distinct value.
    distance = 0.0
    for key in alphabet:
        expected = alphabet[key]
        current = float(my_db[key]) / float(len(string))
        distance += math.pow((current - expected), 2)
    my_db['distance'] = distance
    my_db['match'] = (10 * my_db['trigrams'] + 5 * my_db['bigrams'] +\
                      (1 - my_db['distance']))
    if ((float(my_db['not_in_alphabet']) / float(my_db['length'])) > 0.5):
        my_db['match'] = my_db['match'] -100.0
    
    return my_db


#-------------------------------------------------------------------
# findxorval()
#
# Returns the byte value a string has been XORed with.
#
# The function is based on the assumption that the XORed string
# contain human text and use the given language statistics with
# single letter and bigrams to find the XOR value.
#
# Since the XOR operation always changes a given letter into
# the same other letter, we can find the XOR value by looking
# at the letter frequencies we get for the string for different
# XOR values.
#
# If there are a lot of letters not in the frequency dictionary
# we decide that the string has not been XOR decoded correctly.
#
# For good candidates we calculate a fitness value based on
# the accumulated deviation from the expected frequency.
#-------------------------------------------------------------------
def findxorval(string, language):
    # We start by getting the statistics for the given string
    # as a reference.
    reference = match_string_language(string, language)
    reference['xor_value'] = 0

    # Scan through possible XOR values and keep the one
    # with the best match.
    for xor_value in range(1, 256):
        my_db = {}
        teststring = (xorstring(string, chr(xor_value)))
        my_db = match_string_language(teststring, language)
        my_db['xor_value'] = xor_value
        
        if (my_db['match'] > reference['match']):
            reference.update(my_db)
        
    return reference['xor_value']


#-------------------------------------------------------------------
# xorstring()
#
# Returns a string that consist of the given XORed with the
# given xorstring. If the xorstring is shorter than the given
# input string, the xorstring is applied repeatedly.
#-------------------------------------------------------------------
def xorstring(string, xorstring):
    outstring = ""
    i = 0
    for ch in string:
        outstring += chr(ord(ch) ^ ord(xorstring[i]))
        i = (i + 1) % len(xorstring)
    return outstring


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
# array2hexstring()
#
# Given an array with values, returns a string that represents
# the array including brackets and comma separate hex values.
#-------------------------------------------------------------------
def array2hexstring(hexarray):
    string = "["
    length = len(hexarray)
    
    for i in range(length):
        string += hex(hexarray[i])
        if i < (length - 1):
            string += ", "
    string += "]"
    return string
    

#-------------------------------------------------------------------
# hexstring2string()
#
# Convert a string with hexadecimal values to a string with
# characters having the same values.
#-------------------------------------------------------------------
def hexstring2string(hexstring):
    assert (len(hexstring) % 2 == 0), "String must be even size."
    conv_db = {'0':0x00, '1':0x01,  '2':0x02,  '3':0x03,
               '4':0x04, '5':0x05,  '6':0x06,  '7':0x07,
               '8':0x08, '9':0x09,  'a':0x0a,  'b':0x0b,
               'c':0x0c, 'd':0x0d,  'e':0x0e,  'f':0x0f}

    outstring = ""
    high = 1
    for ch in hexstring:
        assert (ch in conv_db), "\'%c\' not a hexadecimal value." % ch
        if (high == 1):
            tmpval = conv_db[ch] << 4
            high = 0
        else:
            tmpval += conv_db[ch]
            outstring += chr(tmpval)
            high = 1

    return outstring


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
# Test the functions when run separately.
#-------------------------------------------------------------------
def main():
    print "XORstring with sigle character:"
    my_instring = "This is a test string 12345"
    my_xorstring = "1221"
    print "Indata string:"
    print my_instring
    print "Indata string:", my_xorstring
    print "Results:"
    print xorstring(my_instring, my_xorstring)
    print ""
    
    # Test of the string2val function:
    print "String2val:"
    teststring1 = "aa5512deadbeef"
    testval1 = string2val(teststring1)
    print "Teststring =", teststring1
    print "Generated hex array:"
    print array2hexstring(testval1)


    # Test of Base64 converter.
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
    print ""

    print "Test of Hexstring to string:"
    feppel = "++30315465737421"
    print feppel
    print hexstring2string(feppel)
    print ""
    
#-------------------------------------------------------------------
# __name__
# Python thingy to run as a stand alone if called.
#-------------------------------------------------------------------
if __name__ == '__main__':
    main()

#=======================================================================
# EOF CC-functions.py
#=======================================================================
