#!/usr/bin/env python

import tweepy, time, sys
import secret                           # local secret info
from pymarkovchain import MarkovChain

while True:

  try:
    print("Authenticating...")
    auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
    auth.set_access_token(secret.ACCESS_KEY, secret.ACCESS_SECRET)
    api = tweepy.API(auth)

    corpus = ''

    print("Gathering tweets...")
    for page in tweepy.Cursor(api.user_timeline, screen_name=secret.SOURCE_USER).pages(secret.PAGE_COUNT):
      for item in page:
        text = item.text.replace(".", "%2E")
        if len(corpus) == 0:
          corpus = text
        else:
          corpus = corpus + ' ' + text

    print("Setting up Markov chain database...")
    chain = MarkovChain("./markov")
    print("Generating Markov chain database...")
    chain.generateDatabase(corpus)

    # 10 * 15 minutes = API update every 150 minutes
    #  that will change based on new timing between tweets, *shrugs*
    print("Beginning tweet loop.")
    for x in xrange(9):
      print("Tweet " + str(x) + " of tweet loop. (max=9)")
      status = chain.generateString()
      print('Tweet created: "' + status + '"')

      status = status.replace("%2E", ".")
      status = status.replace("&amp;", "&")
      status = status.replace("&lt;", "<")
      status = status.replace("&gt;", ">")
      status = status.replace("@", "")                    # cutting out all @'s entirely
      status = status.replace("twitter.com", "abc.xyz")   # why did I do this?
      print('Tweet modified to "' + status + '".')

      if len(status) > 140:
        status = status[0:136] + '...'
        print('Tweet shortened to: "' + status + '"')

      print("Sending tweet.")
      api.update_status(status=status)
      print("Sleeping for 45 minutes...")
      time.sleep(900*3) #45 minutes

  except tweepy.TweepError, e:
    print(e)
    print("TweepError was caught. Do not be alarmed.")
    #print("Sleeping for 1 hour.")                        # I do this in case everything is fucked
    #time.sleep(3600) #1 hour
    print("Sleeping for a minute.")
    time.sleep(60)
