class RFSettings():
    "This class is used to setup RFCat settings needed for listening, jamming and sending"
    def __init__(self, frequency, baud_rate, channel_bandwidth, modulation_type, upper_rssi, lower_rssi, channel_spacing):

        self.frequency = frequency
        self.baud_rate = baud_rate
        self.channel_bandwidth = channel_bandwidth
        self.modulation_type = modulation_type
        self.upper_rssi = upper_rssi
        self.lower_rssi = lower_rssi
        self.channel_spacing = channel_spacing


    def saveDeviceSettingsTemplate():
        pass

    def loadDeviceSettingsTemplate():
        pass
