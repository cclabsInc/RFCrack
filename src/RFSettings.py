import sys
sys.dont_write_bytecode = True

class RFSettings():
    '''This class is used to setup RFCat settings needed for listening, jamming and sending'''
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
        '''Saves your current RF settings to a file in the device_templates folder which can be loaded in a later attack'''
        with open("./device_templates/"+device_name+".config", 'w') as file:
            for key, value in rf_settings.__dict__.items():
                if not key.startswith("__"):
                    print(f"{str(key)} : {str(value)}")
                    file.write(str(key)+ ":" +str(value) +"\n")
            print(f"Saved file as: ./device_templates/{device_name}.config")

    def loadDeviceSettingsTemplate(self, file_data):
        '''Loads your previously saved working settings for attack against a device'''
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
        '''Prints the current RFCat Settings in use'''
        print ("The following settings are in use:")
        print (f"Frequency: {str(self.frequency)}")
        print (f"Baud_rate: {str(self.baud_rate)}")
        print (f"Channel_bandwidth: {str(self.channel_bandwidth)}")
        print (f"Modulation_type: {str(self.modulation_type)}")
        print (f"Upper_rssi: {str(self.upper_rssi)}")
        print (f"Lower_rssi: {str(self.lower_rssi)}")
        print (f"Channel_spacing: {str(self.channel_spacing)}")
        print (f"Deviation: {str(self.deviation)}")
