import twitter
import auth
import time
from microdotphat import write_string, scroll, clear, show

api = twitter.Api(consumer_key=auth.consumer_key, consumer_secret=auth.consumer_secret, access_token_key=auth.access_token_key, access_token_secret=auth.access_token_secret)

# print api.VerifyCredentials()

t = api.GetUserTimeline(screen_name='@realDonaldTrump', count=1)

tweets = [i.AsDict() for i in t]

clear()
for t in tweets:
    write_string(t['text'])


while True:
    scroll()
    show()
    time.sleep(0.01)
    # print t['text']
