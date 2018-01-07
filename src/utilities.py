import time, os
import findDevices
import RFFunctions as tools
import Clicker

#-----------------Start Log Tailing ----------------#
def logTail(my_clicker):
    ''' This function acts as a linux tail function but only pulling new additions to a file since running
    it parses for payload lines which is uses in analysis and graphing'''
    capture_log = "./captures/capturedClicks.log"
    file = open(capture_log,'r')

    #Find the size of the file and move to the end
    st_results = os.stat(capture_log)
    st_size = st_results[6]
    file.seek(st_size)

    while 1:
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

#-----------------End Log Tailing ----------------#


#-----------------Start De Bruijn Creation ----------------#
def deBruijn(k, n):
    '''This is a function for creating the de Bruijn sequence for bruteforce attacks
    in various lenghts n. Example code aquired from de-bruijn wiki'''
    try:
        _ = int(k)
        alphabet = list(map(str, range(k)))

    except (ValueError, TypeError):
        alphabet = k
        k = len(k)

    a = [0] * k * n
    sequence = []

    def db(t, p):
        if t > n:
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
