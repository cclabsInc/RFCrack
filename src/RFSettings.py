import sys
sys.dont_write_bytecode = True

class RFSettings():
    "This class is used to setup RFCat settings needed for listening, jamming and sending"
    def __init__(self, frequency, baud_rate, channel_bandwidth, modulation_type, upper_rssi, lower_rssi, channel_spacing, deviation):

        self.frequency = frequency
        self.baud_rate = baud_rate
        self.channel_bandwidth = channel_bandwidth
        self.modulation_type = modulation_type
        self.upper_rssi = upper_rssi
        self.lower_rssi = lower_rssi
        self.channel_spacing = channel_spacing
        self.deviation = deviation

    def saveDeviceSettingsTemplate(self, rf_settings, device_name):
        with open("./device_templates/"+device_name+".config", 'w') as file:
            for key, value in rf_settings.__dict__.items():
                if not key.startswith("__"):
                    print(str(key)+ ":" +str(value))
                    file.write(str(key)+ ":" +str(value) +"\n")
            print "Saved file as: ./device_templates/"+device_name+".config"

    def loadDeviceSettingsTemplate(self, file_data):
        for data in file_data:
            if "frequency" in data:
                frequency = self.splitData(data)
                self.frequency = int(frequency)
            elif "baud_rate" in data:
                baud_rate = self.splitData(data)
                self.baud_rate = int(baud_rate)
            elif "channel_bandwidth" in data:
                channel_bandwidth = self.splitData(data)
                self.channel_bandwidth = int(channel_bandwidth)
            elif "modulation_type" in data:
                modulation_type = self.splitData(data)
                self.modulation_type = modulation_type
            elif "upper_rssi" in data:
                upper_rssi = self.splitData(data)
                self.upper_rssi = int(upper_rssi)
            elif "lower_rssi" in data:
                lower_rssi = self.splitData(data)
                self.lower_rssi = int(lower_rssi)
            elif "channel_spacing" in data:
                channel_spacing = self.splitData(data)
                self.channel_spacing = int(channel_spacing)
            elif "deviation" in data:
                deviation = self.splitData(data)
                self.deviation = int(deviation)
        self.printSettings()

    def splitData(self, data):
        key, value = data.split(":")
        value = value.strip()
        return value

    def printSettings(self):
        print "The following settings are in use:"
        print "Frequency: " +str(self.frequency)
        print "Baud_rate: " +str(self.baud_rate)
        print "Channel_bandwidth: " +str(self.channel_bandwidth)
        print "Modulation_type: " +str(self.modulation_type)
        print "Upper_rssi: " +str(self.upper_rssi)
        print "Lower_rssi: " +str(self.lower_rssi)
        print "Channel_spacing: " +str(self.channel_spacing)
        print "Deviation: " +str(self.deviation)
