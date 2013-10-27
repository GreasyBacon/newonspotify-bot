Bot for /r/newonspotify
==============

Introduction
--------------
Initially, I decided to sign up to GitHub to host the code for my first bot written in Python for my subreddit - /r/newonspotify. After thinking about it though, I realised it could also be utilised to post to other social networks such as Tumblr and Twitter. So for the moment, I have accounts created, set-up and working for Tumblr and Twitter, with my next step to be integrating Songkick into the posts for "On Tour" artists.

Purpose
--------------
The purpose of the bot is to act as an auto-submitter of new album/single links to the various social media services that I can set it up for and integrate with.

How it works
--------------
It works in three stages:
- Accessing the Spotify 'lookup' API for albums tagged with 'new' by Spotify (to my knowledge this means albums released within the last week).
- Adding the albums and their information to a local MongoDB to keep a track of which albums have and have not been submitted (as well as which social media networks their links have been submitted to).
- Posting a link to the "http://open.spotify" link of the album on integrated social networks with additional information formatted and included where available.

Requirements
--------------
In order to make this script work as it does, it relies on the following utilities and their respective dependencies:
- pymongo
- urllib2
- simplejson
- praw
- pytumblr
- twython

Limitations
--------------
- At the moment, Twitter is limiting the account status' to 160 per day. This isn't great considering there's a backlog of links to submit to Twitter in my database, and Spotify could tag more than 160 albums as new per day. A potential workaround would be to only submit links to Twitter of artists who have say more than 5,000 followers but currently in the lookup API there's no way to get the number of follwers an artist has. 
- Whenever the script runs, it's just submitting link after link 10 seconds apart. So if you're following the Tumblr or Twitter account, it's just going to keep spamming your feed until the script is done. I may be able to set up a queue system with Tumblr and I'm not worried that much about Reddit, but again Twitter may be an issue. 
- It's just running on my laptop at the moment, with a local database. Ideally, I'd like to move the automated script and database onto a linux server somewhere and keep it running every 6 hours. 
- There probably is more... I just have to think of them.

Updates
--------------
- 23 Oct 2013 - Fixes, script now goes through the first 5 pages of the API results (that should be enough... right?)
- 25 Oct 2013 - Fixes, script now submits to its very own Tumblr blog - newonpsotify.tumblr.com!
- 27 Oct 2013 - Fixes (all day every day), script now submits to its very own Twitter account - @_newonspotify!

Plans for the future
--------------
- Songkick integration (API key acquired!)
- A pot of gold at the end of the rainbow
- Whatever suggestions come my way