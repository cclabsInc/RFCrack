import time, os
from . import findDevices
from . import RFFunctions as tools
from . import Clicker

#-----------------Start Log Tailing ----------------#
def logTail(my_clicker):
    ''' This function acts as a linux tail function but only pulling new additions to a file since running
    it parses for payload lines which is uses in analysis and graphing'''
    capture_log = "./captures/capturedClicks.log"
    try:
        with open(capture_log, 'r') as file:

            #Find the size of the file and move to the end
            st_results = os.stat(capture_log)
            st_size = st_results[6]
            file.seek(st_size)

            while True:
                where = file.tell()
                line = file.readline()
                if not line:
                    time.sleep(1)
                    file.seek(where)
                else:
                    if "found" not in line:
                        presses = tools.parseSignalsLive(line)
                        my_clicker.keyfob_payloads = presses
                        percent = my_clicker.liveClicks()
    
    except IOError as e:
        print(f"Error opening or reading from {capture_log}: {e}")

#-----------------End Log Tailing ----------------#


#-----------------Start De Bruijn Creation ----------------#
def generate_de_bruijn_sequence(k, n):
    '''Generates the de Bruijn sequence for given k and n'''
    if isinstance(k, str):
        alphabet = list(k)
        k = len(alphabet)
    else:
        alphabet = list(map(str, range(k)))

    a = [0] * (k * n)
    sequence = []

    def db(t, p):
        if t == n * k:
            if n % p == 0:
                sequence.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    db(1, 1)
    return "".join(alphabet[i] for i in sequence)

#-----------------End De Bruijn Creation ----------------#

def count_provided_args(args, parser):
    # Count arguments that were explicitly provided by the user
    provided_args = 0
    for action in parser._actions:
        # Skip the help action
        if action.dest == 'help':
            continue
        
        # Check if the argument was provided by the user
        if hasattr(args, action.dest):
            value = getattr(args, action.dest)
            
            # For store_true actions, check if they were explicitly set
            if action.const is not None and value == action.const:
                provided_args += 1
            
            # For other arguments, check if they differ from the default
            elif hasattr(action, 'default'):
                if value != action.default:
                    provided_args += 1
    
    return provided_args
