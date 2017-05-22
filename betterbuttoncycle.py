import datetime
import time
import json
import requests
import os
import auth as au

from predict import predict
from urllib2 import Request, urlopen, URLError
from threading import Thread

import twitter

from microdotphat import write_string, scroll, clear, show, set_decimal
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.IN)
input = GPIO.input(26)

#import ButtonClass

global localtime
global bikestatus
global weatherreport
global busarrival
global twittermessages
global ButtonPresses


class getButtonPresses:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global ButtonPresses
        prev_input = 0
        while self._running:
             #take a reading
             input = GPIO.input(26)
             #if the last reading was low and this one high, print
             if ((not prev_input) and input):
               ButtonPresses = ButtonPresses+1
               print("Button pressed")
             #update previous input
             prev_input = input
             #slight pause to debounce
             time.sleep(0.05)

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
            localtime = t

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

            predictList = []
            for s in stops:
                predictList.append(predict(s))

            time.sleep(4) # Allow a moment for initial results


            currentTime = time.time()
            #print
            for pl in predictList:
                #print pl.data[1] + ' ' + pl.data[3] + ':'
                if pl.predictions: # List of arrival times, in seconds
                    t = pl.predictions[0] - (currentTime - pl.lastQueryTime)
                    busarrival='Bus:'+str(int(t/60))

                else:
                    busarrival='No Bus'

            prevTime = currentTime;
            time.sleep(20)

class getTwitter:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global twittermessages

        while self._running:

            api = twitter.Api(consumer_key=au.consumer_key, consumer_secret=au.consumer_secret, access_token_key=au.access_token_key, access_token_secret=au.access_token_secret)
            t = api.GetUserTimeline(screen_name='@realDonaldTrump', count=5)
            tweets = [i.AsDict() for i in t]
            sum_tweet=''

            for t in tweets:
                sum_tweet=sum_tweet+' - - - '+t['text']

            sum_tweet=sum_tweet.encode(errors='ignore').decode('utf-8')
            twittermessages = sum_tweet
            time.sleep(1000)


if __name__ == '__main__':

    ButtonTrack = getButtonPresses()
    ButtonThread = Thread(target=ButtonTrack.run)
    ButtonThread.start()

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

    TwitterTrack = getTwitter()
    TwitterThread = Thread(target=TwitterTrack.run)
    TwitterThread.start()


    ButtonPresses=0
    localtime=datetime.datetime.now()
    bikestatus='C-sync'
    weatherreport='W-sync'
    busarrival='B-sync'
    twittermessages='T-sync'


    NumberOfModules = 4


    print "ButtonPresses", ButtonPresses
    Exit = False

    while Exit==False:

        #0 Clock
        while(ButtonPresses % NumberOfModules == 0):
            clear()
            show()
            clear()
            if localtime.second % 2 == 0:
                set_decimal(2, 1)
                set_decimal(4, 1)
            else:
                set_decimal(2, 0)
                set_decimal(4, 0)
            write_string(localtime.strftime('%H%M%S'), kerning=False)
            show()
            time.sleep(0.05)
            #print "Clock ", ButtonPresses

        #1 Bike
        while(ButtonPresses % NumberOfModules == 1):
            clear()
            show()
            clear()
            write_string(bikestatus, kerning=False)
            show()
            time.sleep(0.05)
            #print "Bike ", ButtonPresses

        #2 Weather
        while(ButtonPresses % NumberOfModules == 9):
            clear()
            show()
            clear()
            write_string(weatherreport)
            while(ButtonPresses % NumberOfModules == 9):
                scroll()
                show()
            #print "Weather ", ButtonPresses

        #3 Bus
        while(ButtonPresses % NumberOfModules == 2):
            clear()
            show()
            clear()
            write_string(busarrival, kerning=False)
            show()
            time.sleep(0.05)
            #print "Bus ", ButtonPresses

        #4 Twitter
        while(ButtonPresses % NumberOfModules == 9):
            clear()
            show()
            clear()
            write_string(twittermessages)
            while(ButtonPresses % NumberOfModules == 9):
                scroll()
                show()
            #print "Twitter ", ButtonPresses

        #5 OffButton
        while(ButtonPresses % NumberOfModules == 3):
            clear()
            show()
            clear()
            write_string("BYE?", kerning=False)
            show()
            time.sleep(1)
            #print "Offbutton ", ButtonPresses
            if(ButtonPresses % NumberOfModules != 3):
                break

            clear()
            write_string("BYE? 3", kerning=False)
            show()
            time.sleep(1)
            if(ButtonPresses % NumberOfModules != 3):
                break

            clear()
            write_string("BYE? 2", kerning=False)
            show()
            time.sleep(1)
            if(ButtonPresses % NumberOfModules != 3):
                break

            clear()
            write_string("BYE? 1", kerning=False)
            show()
            time.sleep(1)
            if(ButtonPresses % NumberOfModules != 3):
                break

            clear()
            write_string("BYE!", kerning=False)
            show()
            time.sleep(1)
            Exit = True
            break



        # print "CurrentTime", localtime
        # print "BikeStatus", bikestatus
        # print "WeatherReport", weatherreport
        # print "BusArrival", busarrival
        # print "TwitterMessages", twittermessages

    ButtonTrack.terminate()
    TimeTrack.terminate()
    BikeTrack.terminate()
    WeatherTrack.terminate()
    BusTrack.terminate()
    TwitterTrack.terminate()

    GPIO.cleanup()
    print "Shutting down"
    os.system("sudo shutdown now -h")