import twitter
import auth

api = twitter.Api(consumer_key=auth.consumer_key, consumer_secret=auth.consumer_secret, access_token_key=auth.access_token_key, access_token_secret=auth.access_token_secret)

# print api.VerifyCredentials()

t = api.GetUserTimeline('realDonaldTrump', count=5)

tweets = [i.AsDict() for i in t]

for t in tweets:
    print t['text']
