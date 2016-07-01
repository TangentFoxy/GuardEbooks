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
    for page in tweepy.Cursor(api.user_timeline, screen_name='Guard13007').pages(10):
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
    print("Beginning tweet loop.")
    for x in xrange(9):
      print("Tweet " + str(x) + " of tweet loop. (max=9)")
      status = chain.generateString()
      print('Tweet created: "' + status + '".')
      #if status.find("https://t") > -1:
        #status = status.replace("https://t", "https://t.co/8VjFsBJsUA")
      #status = status.replace("http://t", "http://t.co/8VjFsBJsUA")
      status = status.replace("%2E", ".")
      status = status.replace("&amp;", "&")
      status = status.replace("&lt;", "<")
      status = status.replace("&gt;", ">")
      status = status.replace("@", "#")      # changed to hashtags instead of spacing out @'s
        #print('Shortened link auto-completed to Patreon video: "' + status " + '".')
      # shitty fix
      status = status.replace("twitter.com", "abc.xyz")                # why did I do this?
      # fix beginning of link (what the hell is this comment about?)
      print('Tweet modified to "' + status + '".')
      if len(status) > 140:
        status = status[0:136] + '...'
        print('Tweet shortened to: "' + status + '".')
      print("Sending tweet.")
      api.update_status(status=status)
      print("Sleeping for 15 minutes...")
      time.sleep(900) #15 minutes

  except tweepy.TweepError, e:
    print(e)
    print("TweepError was caught. Do not be alarmed.")
    print("Sleeping for 1 hour.")                        # I do this in case everything is fucked
    time.sleep(3600) #1 hour
