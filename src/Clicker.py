import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import sys,subprocess
from . import RFFunctions as tools
sys.dont_write_bytecode = True

#----------Setup Graphing Size-----------#
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 8
fig_size[1] = 3
plt.rcParams["figure.figsize"] = fig_size
#---------End Graphing Size Setup---------#

class Clicker():
    '''This class is used to help identify and analyse signals as well as create clickers
    from captures. It uses a known payload and live captures or a logfile of unknown payloads to compare'''
    def __init__(self, captured_payload, keyfob_payloads=[]):
        self.captured_payload = captured_payload
        self.keyfob_payloads = keyfob_payloads

    def determineDipSwitches(self, captured_payload):
        ''' This function will return the dip switches as up:down:down:up format based on signal analysis'''
        pass

    def liveClicks(self):
        '''Compare Signals and Create graphs to compare a live capture with a keyfob press'''
        count = 0
        live = True
        graphToPercent = {} #Holds % match and payload for each signal in a click

        #Get binary output of the payload
        captured_payload_binary  = self.payloadsToBinary(self.captured_payload)
        print("----------Start Signals In Press--------------")
        for presses in self.keyfob_payloads:
            for keyfob_payload in presses:
                #Get binary output of the keyfob captures
                keyfob_programming_binary = self.payloadsToBinary(keyfob_payload)

                #Handle Calculations for likilihood
                one = ''.join(str(x) for x in captured_payload_binary)
                two =''.join(str(x) for x in keyfob_programming_binary)

                percent = tools.similar(one,two)
                graphToPercent[keyfob_payload] = percent

                print("Percent Chance of Match for press is: %.2f" % percent)
        print("----------End Signals In Press------------")
        #Send dictionaries of percents and return the signal with the highest % comparison
        keyfob_payload = self.getHighestPercent(graphToPercent)
        keyfob_programming_binary = self.payloadsToBinary(keyfob_payload)

        self.createGraph(captured_payload_binary, keyfob_programming_binary)
        self.outputImagesComparisons(1, live)
        plt.close()
        self.openImage('./imageOutput/LiveComparison.png')

        print("For Visual of the last signal comparison go to ./imageOutput/LiveComparison.png")


    def createImageGraph(self):
        '''Create a graph to compare a list of captures with the keyfob press'''
        count = 0
        likilihoods = []
        #Get binary output of the payload
        captured_payload_binary  = self.payloadsToBinary(self.captured_payload)

        for presses in self.keyfob_payloads:
            for keyfob_payload in presses:
                #Get binary output of the keyfob captures
                keyfob_programming_binary = self.payloadsToBinary(keyfob_payload)

                #Handle Calculations for likilihood
                one = ''.join(str(x) for x in captured_payload_binary)
                two =''.join(str(x) for x in keyfob_programming_binary)

                percent = tools.similar(one,two)
                print("Percent Chance of Match for press is: %.2f" % percent)

                self.createGraph(captured_payload_binary, keyfob_programming_binary)
                self.outputImagesComparisons(count)
                count = count+1
                plt.close()

    def setupNumberPrinting(self, captured_payload_binary, keyfob_programming_binary):
        '''prints numbers under the graph, reduces the counts in half for readability with a counter'''
        count = 0
        for tbit, bit in enumerate(captured_payload_binary):
            if (count % 2 != 1):
                plt.text(tbit + 0.5, 3.5, str(bit))
            count = count +1
        count = 0
        for tbit, bit in enumerate(keyfob_programming_binary):
            if (count % 2 != 1):
                plt.text(tbit + 0.5, 1.5, str(bit))
            count = count +1

    def outputImagesComparisons(self, count, live=False):
        '''Outputs image files to compare capture to keyfob presses'''
        if live:
            pylab.savefig("./imageOutput/LiveComparison.png")
        else:
            pylab.savefig("./imageOutput/Graph"+str(count)+".png")


    def payloadsToBinary(self, payload):
        '''Converts hex data into binary and back into lists of binary numbers'''
        binary = bin(int(payload,16))[2:]
        results = map(int,list(str(binary)))
        return results

    def getHighestPercent(self, myDictionary):
        ''' Takes a dictonary of signals as keys and returns the signal with the highest percent value'''
        highest_percent = max(zip(myDictionary.values(), myDictionary.keys()))
        return highest_percent[1]

    def openImage(self, path):
        '''Opens and image from the hardrive based on the path sent in'''
        imageViewerFromCommandLine = {'linux':'eog',
                                      'linux2':'eog',
                                      'win32':'explorer',    #doubt this works in windows but leaving it here for now
                                      'darwin':'open'}[sys.platform]
        subprocess.call([imageViewerFromCommandLine, path])

    def createGraph(self, captured_payload_binary, keyfob_programming_binary):
        '''Sets up the graphing elements for images or display, requires 2 binary payloads to plot'''
        payload_data = np.repeat(captured_payload_binary, 2)
        keyfob_data = np.repeat(keyfob_programming_binary, 2)
        t = 0.5 * np.arange(len(payload_data))
        u = 0.5 * np.arange(len(keyfob_data))

        #Used to show the wave form
        plt.step(t, payload_data + 4, 'r', linewidth = 2, where='post')
        plt.step(u, keyfob_data + 2, 'r', linewidth = 2, where='post')

        #Limit the height of the waveform and turns off axis lines
        plt.ylim([-1,6])
        plt.gca().axis('off')
