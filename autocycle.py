import datetime
import time
import json
import requests
import auth as au
from predict import predict
from urllib2 import Request, urlopen, URLError
from threading import Thread

global localtime
global bikestatus
global weatherreport
global busarrival


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

class getWeather:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global weatherreport
        while self._running:
            secret = au.DarkSkySecret
            lat = str(au.lat)
            lon = str(au.lon)

            request = Request('https://api.darksky.net/forecast/'+secret+'/'+lat+','+lon+'?exclude=[minutely,hourly]')
            try:
              response = urlopen(request)
              currentweather = response.read()
                # print currentweather
            except URLError, e:
                print 'No Weather. Got an error code:', e

            weatherdata = json.loads(currentweather)
            #pprint(weatherdata)
            summary=str(weatherdata['daily']['data'][0]['summary'])
            maxTemperature = str(int(round((weatherdata['daily']['data'][0]['temperatureMax'] - 32.)*5./9.))) #in degrees C
            minTemperature = str(int(round((weatherdata['daily']['data'][0]['temperatureMin'] - 32.)*5./9.))) #in degrees C
            precipProbability = str(int(round(weatherdata['daily']['data'][0]['precipProbability']*100.)))

            weatherreport="Weather: "+summary+" Min/Max Temp: "+minTemperature+"/"+maxTemperature+"C, Rain: "+precipProbability+"% - - -"
            time.sleep(3600)

class getBus:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global busarrival
        while self._running:
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
                    #for p in pl.predictions:
                        # Extrapolate from predicted arrival time,
                        # current time and time of last query,
                        # display in whole minutes.
                    t = pl.predictions[0] - (currentTime - pl.lastQueryTime)
                    busarrival='Bus:'+str(int(t/60))
                    #Output.encode(errors='ignore').decode('utf-8')

                else:
                    busarrival='No Bus'
                    #Output.encode(errors='ignore').decode('utf-8')

            prevTime = currentTime;
            time.sleep(60)


TimeTrack = getTime()
TimeThread = Thread(target=TimeTrack.run)
TimeThread.start()

BikeTrack = getBike()
BikeThread = Thread(target=BikeTrack.run)
BikeThread.start()

WeatherTrack = getWeather()
WeatherThread = Thread(target=WeatherTrack.run)
WeatherThread.start()

BusTrack = getBus()
BusThread = Thread(target=BusTrack.run)
BusThread.start()

cycle=0

localtime='0'
bikestatus='C-sync'
weatherreport='W-sync'
busarrival='B-sync'



Exit = False #Exit flag

while Exit==False:
 cycle = cycle + 1
 print "CurrentTime", localtime
 print "BikeStatus", bikestatus
 print "WeatherReport", weatherreport
 print "BusArrival", busarrival
 time.sleep(1) #One second delay
 if (cycle > 10): Exit = True #Exit Program

TimeTrack.terminate()
BikeTrack.terminate()
WeatherTrack.terminate()
BusTrack.terminate()

print "Goodbye :)"
