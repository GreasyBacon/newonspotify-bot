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