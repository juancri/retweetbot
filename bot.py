# Copyright (c) 2012 Juan C. Olivares <juancri@juancri.com>
# based on original code by Christian Palomares <palomares.c@gmail.com>
# 
# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 

import time
import twitter

# config
friends = [ 1, 2, 3 ] # Add here the IDs of the users who will be retweeted
hashtag = '#myhashtag' # Any hashtag or magic word that triggers the retweet
sleep = 60 # Time betweet queries to Twitter
count = 100 # Amount of tweets per request (max 100)

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
	timeline = api.GetFriendsTimeline (since_id = lastid, count = count)
	
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
		retweet = 'RT @' + status.user.screen_name + ": " + status.text
		if len (retweet) > 140:
			retweet = retweet [:137] + "..."
		print "Tweeting:", retweet
		api.PostUpdate (retweet)

        # zZzZzZ
        time.sleep (sleep)
