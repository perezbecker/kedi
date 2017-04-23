import json
import requests
from microdotphat import write_string, scroll, clear, show

#def getHubwayStatus():

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

BikeStatus='E'+str(min(9,BikesErie))+'V'+str(min(9,BikesVassar))+'K'+str(min(9,DocksKendallT+DocksKendallT2))
#print BikeStatus

while True:
    clear()
    write_string(BikeStatus, kerning=False)
    show()
