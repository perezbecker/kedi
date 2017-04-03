# Super simple NextBus display thing (prints to console).

import time
from predict import predict
from microdotphat import write_string, scroll, clear, show

# List of bus lines/stops to predict.  Use routefinder.py to look up
# lines/stops for your location, copy & paste results here.  The 4th
# element on each line can then be edited for brevity if desired.
stops = [
  ( 'mbta', '47', '1812', 'Central Square' ), #47 stop Brookline/Putnam, towards Central Square
]

# Populate a list of predict objects from stops[].  Each then handles
# its own periodic NextBus server queries.  Can then read or extrapolate
# arrival times from each object's predictions[] list (see code later).
predictList = []
for s in stops:
    predictList.append(predict(s))

time.sleep(4) # Allow a moment for initial results


currentTime = time.time()
#print
for pl in predictList:
    #print pl.data[1] + ' ' + pl.data[3] + ':'
    if pl.predictions: # List of arrival times, in seconds
        for p in pl.predictions:
            # Extrapolate from predicted arrival time,
            # current time and time of last query,
            # display in whole minutes.
            t = p - (currentTime - pl.lastQueryTime)
            Output='Bus:'+str(int(t/60))
            #Output.encode(errors='ignore').decode('utf-8')

        else:
            Output='No Bus'
            #Output.encode(errors='ignore').decode('utf-8')

prevTime = currentTime;
#time.sleep(5) # Refresh every ~5 seconds


while True:
    clear()
    write_string(Output, kerning=False)
    show()
