from threading import Thread
import datetime
import time
import json
import requests

global localtime
global bikestatus


class getTime:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global localtime
        while self._running:
            time.sleep(0.05)
            t = datetime.datetime.now()
            # if t.second % 2 == 0:
            #     set_decimal(2, 1)
            #     set_decimal(4, 1)
            # else:
            #     set_decimal(2, 0)
            #     set_decimal(4, 0)

            localtime = t.strftime('%H%M%S')

class getBike:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global bikestatus
        while self._running:
            data={}
            json_data=json.dumps(data)
            url="https://secure.thehubway.com/data/stations.json"
            headers = {'Content-Type' : 'application/json'}
            response = requests.get(url,data=json_data, headers=headers)
            parsedjson = json.loads(response.text)

            StationCode=[]
            BikesAvailable=[]
            DocksAvailable=[]

            for i in range(len(parsedjson['stations'])):
                StationCode.append(str(parsedjson['stations'][i]['n']))
                BikesAvailable.append(int(parsedjson['stations'][i]['ba']))
                DocksAvailable.append(int(parsedjson['stations'][i]['da']))

            ErieCode='M32047'
            VassarCode='M32042'
            KendallTCode='M32004'
            KendallT2Code='M32003'

            BikesErie=BikesAvailable[StationCode.index(ErieCode)]
            BikesVassar=BikesAvailable[StationCode.index(VassarCode)]
            DocksKendallT=DocksAvailable[StationCode.index(KendallTCode)]
            DocksKendallT2=DocksAvailable[StationCode.index(KendallT2Code)]

            bikestatus='E'+str(min(9,BikesErie))+'V'+str(min(9,BikesVassar))+'K'+str(min(9,DocksKendallT+DocksKendallT2))
            time.sleep(60)


TimeTrack = getTime()
TimeThread = Thread(target=TimeTrack.run)
TimeThread.start()

BikeTrack = getBike()
BikeThread = Thread(target=BikeTrack.run)
BikeThread.start()



cycle=0

localtime='0'
bikestatus='sync..'



Exit = False #Exit flag

while Exit==False:
 cycle = cycle + 1
 print "CurrentTime", localtime
 print "BikeStatus", bikestatus
 time.sleep(1) #One second delay
 if (cycle > 10): Exit = True #Exit Program

TimeTrack.terminate()
BikeTrack.terminate()

print "Goodbye :)"
