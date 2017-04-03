import time
from datetime import datetime
from urllib2 import Request, urlopen, URLError
import json
import auth as au
from microdotphat import write_string, scroll, clear, show

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

Output="Weather: "+summary+" Min/Max Temp: "+minTemperature+"/"+maxTemperature+"C, Rain: "+precipProbability+"% - - -"


clear()
write_string(Output)



while True:
    scroll()
    show()
