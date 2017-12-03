from rflib import *
import time, re, sys

capture = ""

def bruteForceFreq(d, rf_settings, interval):
    '''Brute Forces frequencies looking for one with data being sent
       Requires a RFCat Class, a starting frequency and the incrementing interval
       EX: 315000000, 50000'''
    d.setFreq(rf_settings.frequency)
    current_freq = rf_settings.frequency

    while not keystop():
        print "Currently Scanning: " + str(current_freq)+ " To cancel hit enter and wait a few seconds"
        sniffFrequency(d)

        current_freq +=interval
        d.setFreq(current_freq)



def searchKnownFreqs(d, known_frequencies):
    '''Sniffs on a rotating list of known frequences from the default list
        or optionally uses a list provided to the function requires an RFCat class'''

    while not keystop():

        for current_freq in known_frequencies:
            d.setFreq(current_freq)
            print "Currently Scanning: " + str(current_freq)+" To cancel hit enter and wait a few seconds"
            print
            sniffFrequency(d)



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
