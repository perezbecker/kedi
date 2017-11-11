import socket

hostname=socket.gethostname()

if(hostname == "kedi0"):
    lat = 42.3601
    lon = -71.09
    busstation = ( 'mbta', '47', '1812', 'Central Square' ) #47 stop Brookline/Putnam, towards Central Square
    altTimeZone = "UTC" #UTC only at this point
    twitter = ["@realDonaldTrump",3]
    bike1Letter, bike1Type, bike1Codes = "E", "Pickup",  ["M32047"] #Erie
    bike2Letter, bike2Type, bike2Codes = "V", "Pickup",  ["M32042"] #Vassar
    bike3Letter, bike3Type, bike3Codes = "K", "Dropoff", ["M32004","M32003","M32053"] #All 3 by Kendall
    StreetsweepNthWeek_Weekday = [1,4] #First Friday of Month 

elif(hostname == "kedi1"):
    lat = 42.3601
    lon = -71.09
    busstation = ( 'mbta', '47', '1812', 'Central Square' ) #47 stop Brookline/Putnam, towards Central Square
    altTimeZone = "UTC" #UTC only at this point
    twitter = ["@realDonaldTrump",3]
    bike1Letter, bike1Type, bike1Codes = "M", "Pickup",  ["M32053"] #Memorial
    bike2Letter, bike2Type, bike2Codes = "K", "Pickup",  ["M32004","M32003"] #Kendal 1+2
    bike3Letter, bike3Type, bike3Codes = "E", "Dropoff", ["M32047","M32042"] #Erie and Vassar
    StreetsweepNthWeek_Weekday = [1,4] #First Friday of Month 

elif(hostname == "kedi2"):
    lat = 42.3601
    lon = -71.09
    busstation = ( 'mbta', '47', '1812', 'Central Square' ) #47 stop Brookline/Putnam, towards Central Square
    altTimeZone = "UTC" #UTC only at this point
    twitter = ["@BarackObama",3]
    bike1Letter, bike1Type, bike1Codes = "B", "Pickup",  ["A32003"] #BU
    bike2Letter, bike2Type, bike2Codes = "T", "Dropoff", ["M32022"] #Trader Joes
    bike3Letter, bike3Type, bike3Codes = "M", "Dropoff", ["M32053"] #Memorial
    StreetsweepNthWeek_Weekday = [1,4] #First Friday of Month 
    
elif(hostname == "kedi3"):
    lat = 42.3601
    lon = -71.09
    busstation = ( 'mbta', '47', '1812', 'Central Square' ) #47 stop Brookline/Putnam, towards Central Square
    altTimeZone = "UTC" #UTC only at this point
    twitter = ["@realDonaldTrump",3]
    bike1Letter, bike1Type, bike1Codes = "M", "Pickup",  ["M32053"] #Memorial
    bike2Letter, bike2Type, bike2Codes = "K", "Pickup",  ["M32004","M32003"] #Kendal 1+2
    bike3Letter, bike3Type, bike3Codes = "E", "Dropoff", ["M32047","M32042"] #Erie and Vassar
    StreetsweepNthWeek_Weekday = [1,4] #First Friday of Month 
