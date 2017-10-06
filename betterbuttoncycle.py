import sys, os
sys.path.append(os.path.dirname(__file__))
from datetime import datetime, timedelta
from calendar import mdays
import time
import json
import requests
import os
import auth as au

from predict import predict
from urllib2 import Request, urlopen, URLError
from threading import Thread, enumerate

import twitter

from microdotphat import write_string, scroll, scroll_to, clear, show, set_decimal
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.IN)
input = GPIO.input(26)

#import ButtonClass

global localtime
global utctime
global bikestatus
global weatherreport0
global weatherreport1
global busarrival
global twittermessages
global ButtonPresses
global daysTilSweep


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
            t = datetime.now()
            localtime = t

class getUTCTime:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global utctime
        while self._running:
            time.sleep(0.05)
            t = datetime.utcnow()
            utctime = t


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
            #print("Completed Bike thread")
            time.sleep(60)

class getWeather:
    def __init__(self,day):
        self._running = True
        self.day=day

    def terminate(self):
        self._running = False

    def run(self):
        global weatherreport0
        global weatherreport1

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
            if(self.day=="Today"):
                wheatherindex=0
            if(self.day=="Tomorrow"):
                wheatherindex=1

            summary=str(weatherdata['daily']['data'][wheatherindex]['summary'])
            maxTemperature = str(int(round((weatherdata['daily']['data'][wheatherindex]['temperatureMax'] - 32.)*5./9.))) #in degrees C
            minTemperature = str(int(round((weatherdata['daily']['data'][wheatherindex]['temperatureMin'] - 32.)*5./9.))) #in degrees C
            precipProbability = str(int(round(weatherdata['daily']['data'][wheatherindex]['precipProbability']*100.)))

            if(self.day=="Today"):
                weatherreport0="- - - Today's Weather: "+summary+" Min/Max Temp: "+minTemperature+"/"+maxTemperature+"C, Rain: "+precipProbability+"% "
            if(self.day=="Tomorrow"):
                weatherreport1="- - - Tomorrow's Weather: "+summary+" Min/Max Temp: "+minTemperature+"/"+maxTemperature+"C, Rain: "+precipProbability+"% "
            time.sleep(3600)

class getBus:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global busarrival

        stop = [
          ( 'mbta', '47', '1812', 'Central Square' ), #47 stop Brookline/Putnam, towards Central Square
        ]

        BusPrediction=predict(stop[0])

        while self._running:


            time.sleep(60) # Allow a moment for results

            LetterTime=["A","B","C","D","E","F"]
            currentTime = time.time()
            #print BusPrediction.predictions

            try:
                t1 = BusPrediction.predictions[0] - (currentTime - BusPrediction.lastQueryTime)

                if(t1<600 and t1>=0):
                    t1string = str(int(t1/60))+LetterTime[int((t1%60)/10)]
                elif(t1<0):
                    t1string="<0"
                elif(t1>5940):
                    t1string="++"
                else:
                    t1string=str(int(t1/60))

                try:
                    t2 = BusPrediction.predictions[1] - (currentTime - BusPrediction.lastQueryTime)

                    if(t2<600 and t2>=0):
                        t2string = str(int(t2/60))+LetterTime[int((t2%60)/10)]
                    elif(t2<0):
                        t2string="<0"
                    elif(t2>5940):
                        t2string="++"
                    else:
                        t2string=str(int(t2/60))

                    busarrival=t1string+','+t2string+'.'
                except:
                    busarrival='Bus:'+t1string
            except:
                busarrival='No Bus'

            #print("Completed Bus thread")


class getTwitter:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global twittermessages

        while self._running:

            api = twitter.Api(consumer_key=au.consumer_key, consumer_secret=au.consumer_secret, access_token_key=au.access_token_key, access_token_secret=au.access_token_secret)
            t = api.GetUserTimeline(screen_name='@realDonaldTrump', count=3)
            tweets = [i.AsDict() for i in t]
            sum_tweet=''

            for t in tweets:
                sum_tweet=sum_tweet+' - - - '+t['text']

            sum_tweet=sum_tweet.encode(errors='ignore').decode('utf-8')
            twittermessages = sum_tweet
            time.sleep(1000)


class daysUntilStreetSweep:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global daysTilSweep

        while self._running:

            the_date=datetime.now()
            nth_week=1
            week_day=4 #First Friday of Month

            temp = the_date.replace(day=1)
            adj = (week_day - temp.weekday()) % 7
            temp += timedelta(days=adj)
            temp += timedelta(weeks=nth_week-1)
            firstOption = (temp - the_date).days
            if(firstOption >= 0):
                daysTilSweep = 'Car:'+str(firstOption)
            else:
                new_date_temp=the_date.replace(day=1)
                new_date=new_date_temp + timedelta(mdays[new_date_temp.month])
                temp2 = new_date.replace(day=1)
                adj2 = (week_day - temp2.weekday()) % 7
                temp2 += timedelta(days=adj2)
                temp2 += timedelta(weeks=nth_week-1)
                secondOption = (temp2 - the_date).days
                daysTilSweep = 'Car:'+str(secondOption)

            time.sleep(1000)


if __name__ == '__main__':

    ButtonPresses=0
    localtime=datetime.now()
    utctime=datetime.utcnow()
    bikestatus='C-sync'
    weatherreport0='W-sync'
    weatherreport1='W-sync'
    busarrival='B-sync'
    twittermessages='T-sync'
    daysTilSweep='S-sync'

    NumberOfModules = 9


    #print "ButtonPresses", ButtonPresses
    Exit = False

    while Exit==False:

        ButtonTrack = getButtonPresses()
        ButtonThread = Thread(target=ButtonTrack.run)
        ButtonThread.start()

        TimeTrack = getTime()
        TimeThread = Thread(target=TimeTrack.run)
        TimeThread.start()

        UTCTimeTrack = getUTCTime()
        UTCTimeThread = Thread(target=UTCTimeTrack.run)
        UTCTimeThread.start()

        BikeTrack = getBike()
        BikeThread = Thread(target=BikeTrack.run)
        BikeThread.start()

        WeatherTrack0 = getWeather("Today")
        WeatherThread0 = Thread(target=WeatherTrack0.run)
        WeatherThread0.start()

        WeatherTrack1 = getWeather("Tomorrow")
        WeatherThread1 = Thread(target=WeatherTrack1.run)
        WeatherThread1.start()

        BusTrack = getBus()
        BusThread = Thread(target=BusTrack.run)
        BusThread.start()

        TwitterTrack = getTwitter()
        TwitterThread = Thread(target=TwitterTrack.run)
        TwitterThread.start()

        SweepTrack = daysUntilStreetSweep()
        SweepThread = Thread(target=SweepTrack.run)
        SweepThread.start()

        print "* * * RESTARTING THREADS * * *"
        for thread in threading.enumerate():
            print(thread.name)

        t_end = time.time() + 60 * 2

        while (time.time() < t_end and Exit==False):


            print "BikeStatus", bikestatus
            print "BusArrival", busarrival
            print "MoveCar", daysTilSweep
            print "TodaysWeatherReport", weatherreport0
            print "TomorrowsWeatherReport", weatherreport1
            print "TwitterMessages", twittermessages

            #0 Clock
            while(ButtonPresses % NumberOfModules == 0):
                clear()
                scroll_to(0,0)
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

            #1 UTCClock
            while(ButtonPresses % NumberOfModules == 1):
                clear()
                scroll_to(0,0)
                if utctime.second % 2 == 0:
                    set_decimal(2, 1)
                    set_decimal(4, 1)
                else:
                    set_decimal(2, 0)
                    set_decimal(4, 0)
                write_string(utctime.strftime('%H%M%S'), kerning=False)
                show()
                time.sleep(0.05)
                #print "Clock ", ButtonPresses

            #2 Bike
            while(ButtonPresses % NumberOfModules == 2):
                clear()
                scroll_to(0,0)
                write_string(bikestatus, kerning=False)
                show()
                time.sleep(0.05)
                #print "Bike ", ButtonPresses


            #3 Bus
            while(ButtonPresses % NumberOfModules == 3):
                clear()
                scroll_to(0,0)
                write_string(busarrival, kerning=False)
                show()
                time.sleep(0.05)
                #print "Bus ", ButtonPresses

            #4 StreetSweep
            while(ButtonPresses % NumberOfModules == 4):
                clear()
                scroll_to(0,0)
                write_string(daysTilSweep, kerning=False)
                show()
                time.sleep(0.05)


            #5 Offbutton
            while(ButtonPresses % NumberOfModules == 5):
                clear()
                scroll_to(0,0)
                write_string("BYE?", kerning=False)
                show()
                time.sleep(1)
                #print "Offbutton ", ButtonPresses
                if(ButtonPresses % NumberOfModules != 5):
                    break

                clear()
                scroll_to(0,0)
                write_string("BYE? 3", kerning=False)
                show()
                time.sleep(1)
                if(ButtonPresses % NumberOfModules != 5):
                    break

                clear()
                scroll_to(0,0)
                write_string("BYE? 2", kerning=False)
                show()
                time.sleep(1)
                if(ButtonPresses % NumberOfModules != 5):
                    break

                clear()
                scroll_to(0,0)
                write_string("BYE? 1", kerning=False)
                show()
                time.sleep(1)
                if(ButtonPresses % NumberOfModules != 5):
                    break

                clear()
                write_string("BAIBAI", kerning=False)
                show()
                time.sleep(1)
                Exit = True
                break

            #6 TodaysWeather
            while(ButtonPresses % NumberOfModules == 6):
                clear()
                scroll_to(0,0)
                write_string(weatherreport0)
                while(ButtonPresses % NumberOfModules == 6):
                    scroll()
                    show()
                #print "Weather ", ButtonPresses

            #7 TomorrowsWeather
            while(ButtonPresses % NumberOfModules == 7):
                clear()
                scroll_to(0,0)
                write_string(weatherreport1)
                while(ButtonPresses % NumberOfModules == 7):
                    scroll()
                    show()
                #print "Weather ", ButtonPresses

            #8 Twitter
            while(ButtonPresses % NumberOfModules == 8):
                clear()
                scroll_to(0,0)
                write_string(twittermessages)
                while(ButtonPresses % NumberOfModules == 8):
                    scroll()
                    show()
                #print "Twitter ", ButtonPresses


            # print "CurrentTime", localtime
            # print "BikeStatus", bikestatus
            # print "WeatherReport", weatherreport
            # print "BusArrival", busarrival
            # print "TwitterMessages", twittermessages

        clear()
        scroll_to(0,0)
        show()
        ButtonTrack.terminate()
        TimeTrack.terminate()
        BikeTrack.terminate()
        WeatherTrack.terminate()
        BusTrack.terminate()
        TwitterTrack.terminate()
        SweepTrack.terminate()

    GPIO.cleanup()
    print "Shutting down"
    os.system("sudo shutdown now -h")
