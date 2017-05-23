from datetime import datetime, timedelta
from calendar import mdays


nth_week=1
week_day=4 #First Friday of Month

today=datetime(2017,11,4)

def daysUntilStreetSweep(the_date,nth_week,week_day):
    temp = the_date.replace(day=1)
    adj = (week_day - temp.weekday()) % 7
    temp += timedelta(days=adj)
    temp += timedelta(weeks=nth_week-1)
    firstOption = (temp - the_date).days
    if(firstOption >= 0):
        return firstOption
    else:
        new_date_temp=the_date.replace(day=1)
        new_date=new_date_temp + timedelta(mdays[new_date_temp.month])
        temp2 = new_date.replace(day=1)
        adj2 = (week_day - temp2.weekday()) % 7
        temp2 += timedelta(days=adj2)
        temp2 += timedelta(weeks=nth_week-1)
        secondOption = (temp2 - the_date).days
        return secondOption

print daysUntilStreetSweep(today, nth_week, week_day)
