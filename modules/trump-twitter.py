import twitter
import auth
import time
from microdotphat import write_string, scroll, clear, show

api = twitter.Api(consumer_key=auth.consumer_key, consumer_secret=auth.consumer_secret, access_token_key=auth.access_token_key, access_token_secret=auth.access_token_secret)

# print api.VerifyCredentials()

t = api.GetUserTimeline(screen_name='@realDonaldTrump', count=5)

tweets = [i.AsDict() for i in t]

sum_tweet=''

for t in tweets:
    sum_tweet=sum_tweet+' - - - '+t['text']

sum_tweet=sum_tweet.encode(errors='ignore').decode('utf-8')

clear()
write_string(sum_tweet)

timeout = time.time() + 60*4 #Timeout every four minutes

while True:
    scroll()
    show()
    if time.time() > timeout:
        break
    #time.sleep(0.01)
    # print t['text']
