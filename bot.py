# 
# Copyright (c) 2012 Juan C. Olivares <juancri@juancri.com>
# based on original code by Christian Palomares <palomares.c@gmail.com>
# 
# Distributed under the MIT/X11 license. Check LICENSE for details.
# 

import time
import twitter

# config
friends = [ 1, 2, 3 ] # Add here the IDs of the users who will be retweeted
hashtag = '#myhashtag' # Any hashtag or magic word that triggers the retweet
sleep = 60 # Time betweet queries to Twitter
count = 100 # Amount of tweets per request (max 100)
nativeRetweet = True # If true, retweets natively. If false, retweets using "RT @user:" 

# API initialization
# WARNING: Don't share these keys
api = twitter.Api (
	consumer_key = '',
	consumer_secret = '',
	access_token_key = '',
	access_token_secret = '')

# loop
lastid = None
first = 1
while 1:
	# get last tweets
	print "Getting tweets..."
	timeline = api.GetHomeTimeline (since_id = lastid, count = count)
	
	# update last ID
	if len (timeline) > 0:
		lastid = timeline [0].id
		print "Last ID updated:", lastid
	
	# skip the first time
	if first > 0:
		first = 0
		continue
	
	# check tweets
	for status in timeline:
		# is the user allowed?
		if not status.user.id in friends:
			continue
		
		# has the hashtag?
		if status.text.lower ().find (hashtag) < 0:
			continue
		
		# let's retweet
		if nativeRetweet:
			print "Retweeting:", status.user.screen_name, status.text
			api.PostRetweet (status.id)
		else:
			retweet = 'RT @' + status.user.screen_name + ": " + status.text
			if len (retweet) > 140:
				retweet = retweet [:137] + "..."
			print "Tweeting:", retweet
			api.PostUpdate (retweet)

        # zZzZzZ
        time.sleep (sleep)
