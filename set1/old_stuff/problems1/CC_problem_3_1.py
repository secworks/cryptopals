#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#=======================================================================
#
# CC-problem_3_1.py
# -----------------
# Python solution to problem 3 in set 1 of the Matasano
# Crypto Challenges.
#
#
# Problem description:
#
# Single-character XOR Cipher
# 
# The hex encoded string:
# 
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# 
# ... has been XOR'd against a single character. Find the key, decrypt
# the message.
# 
# Write code to do this for you. How? Devise some method for "scoring"
# a piece of English plaintext. (Character frequency is a good metric.)
# Evaluate each output and choose the one with the best score.
# 
# Tune your algorithm until this works.
#
#
# Observation:
# Should probably state if the string is mixed case or not.
#
#
# (c) 2012 Secworks Sweden AB
# Joachim Strombergson
#
#=======================================================================

import CC_functions
import math

#-------------------------------------------------------------------
# num_bigrams()
#
# Given a string and a list of bigrams returns the total number
# of bigrams in the string.
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
        teststring = (CC_functions.xorstring(string, chr(xor_value)))
        my_db = match_string_language(teststring, language)
        my_db['xor_value'] = xor_value
        
        if (my_db['match'] > reference['match']):
            reference.update(my_db)
        
    return reference['xor_value']

    
#-------------------------------------------------------------------
# main()
#
# Run the functions to solve the problem with the given test case.
#-------------------------------------------------------------------
def main():
    instring = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

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

    print "CC Problem 3_1."
    print "The given XOR encoded string:"
    print instring
    xor_value = findxorval(CC_functions.hexstring2string(instring), eng_lang)
    print "The string was XOR encoded using byte value 0x%02x" % xor_value
    print "Decoded string:"
    print CC_functions.xorstring(CC_functions.hexstring2string(instring), chr(xor_value))
    print ""


#-------------------------------------------------------------------
# __name__
# Python thingy to run as a stand alone if called.
#-------------------------------------------------------------------
if __name__ == '__main__':
    main()

#=======================================================================
# EOF CC_problem_2_1.py
#=======================================================================
