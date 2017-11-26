from rflib import *
import time, re, sys

capture = ""

def bruteForceFreq(d, starting_frequency, interval):
    '''Brute Forces frequencies looking for one with data being sent
       Requires a RFCat Class, a starting frequency and the incrementing interval
       EX: 315000000, 50000'''
    d.setFreq(starting_frequency)
    current_freq = starting_frequency
    try:
        while True:
            print "Currently Scanning: " + str(current_freq)+ " To cancel hit CTRL-Z and unplug yardstick"
            sniffFrequency(d)

            current_freq +=interval
            d.setFreq(current_freq)
    except KeyboardInterrupt:
        sys.exit()  #does not seem to work.. FTW


def searchKnownFreqs(d, known_frequencies):
    '''Sniffs on a rotating list of known frequences from the default list
        or optionally uses a list provided to the function requires an RFCat class'''
    try:
        while True:

            for current_freq in known_frequencies:
                d.setFreq(current_freq)
                print "Currently Scanning: " + str(current_freq)+" To cancel hit CTRL-Z and unplug yardstick"
                print
                sniffFrequency(d)
    except KeyboardInterrupt:
        sys.exit()  #does not seem to work.. FTW


def sniffFrequency(d):
    ''' Sniffs on a frequency, requires a RFCat Class with proper info set for listening'''

    try:
        y, z = d.RFrecv(timeout=3000)
        capture = y.encode('hex')
        print capture
        #mytime +=1
    except ChipconUsbTimeoutException:
        pass

    return
