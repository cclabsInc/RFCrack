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
-----------------------------------------------------------
Developer: @Ficti0n - CCLabs.io / ConsoleCowboys.com
Blog: console-cowboys.blogspot.com
YouTube Tutorial: <Add Link Here>
Release: 1.0


RFCrack was developed for testing RF communications between any physical device that
communicates over sub Ghz frequencies. IoT devices, Cars, Alarm Systems etc... Testing was
done with the Yardstick One on OSX, but RFCrack should work fine in linux.
Support for other RF related testing will be added as needed in my testing. I am currently researching
keyless Entry bypasses. Keyless entry functionality will be added in the future with additional hardware
requirements for advanced attacks.

Feel free to use this software as is for personal use only. Do not use this code in other projects
or in commercial products. I hold no liability for your actions with this code.
Your life choices are your own.


Current supported Functionality:
--------------------------------
- Replay attacks -i -f
- Send Saved Payloads -s -u
- Rolling code bypass attacks -r -f
- Targeted -t -f
- Jamming -j -f
- Scanning incrementally through frequencies -b -v -f
- Scanning common frequencies -k

Future Functionality(Currently Researching)
-------------------------------------------
- Keyless Entry/EngineStart bypass with SDR
- Any Suggestions based on realistic use-cases you want me to add??  


Usage Examples:
---------------
Live Replay::        python RFCrack.py -i
Rolling Code::       python RFCrack.py -r -m MOD_2FSK -f 314350000
Jamming::            python RFCrack.py -j -f 314000000
Scan Common::        python RFCrack.py -k
Scan your List::     python RFCrack.py -k -z 433000000 314000000 390000000
Incremental Scan::   python RFCrack.py -b -v 5000000
Send Saved Payload:: python RFCrack.py -s -u ./files/test.cap -f 315000000 -m MOD_ASK_OOK

Useful arguments:
------------------------
-m Change modulation, usually MOD_2FSK or MOD_ASK_OOK
-s Send packet from a file source
-f Change the frequency used in attacks

Other Notes:
------------------------
Captures get saved to ./files directory by default!

Rolling code is hit or miss due to its nature with jamming and sniffing at the same time,
but it works. Just use the keyfob near the yardsticks. It will also require 2 yardsticks,
one for sniffing while the other one is jamming.

And a final note, this is my own test bench for doing research and dev, if you have ideas
to make it better based on realistic use case scenarios, feel free to reach out to me.
Right now I am working on keyless entry attacks which I will implement into this later. 
