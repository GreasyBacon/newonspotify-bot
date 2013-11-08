Bot for /r/newonspotify
==============

Introduction
--------------
Initially, I decided to sign up to GitHub to host the code for my first bot written in Python for my subreddit - /r/newonspotify. After thinking about it though, I realised it could also be utilised to post to other social networks such as Tumblr and Twitter. So, at the moment I have the script/bot posting to Reddit, Twitter and Tumblr, with recently added Songkick integration for Tumblr/Reddit posts, and Tiny.cc URL shortening integrated for Twtitter posts. 

Purpose
--------------
The purpose of the bot is to act as an auto-submitter of new album/single links to the various social media services that I can set it up for and integrate with.

How it works
--------------
It works by going through the following stages:
- Accessing the Spotify 'lookup' API for albums tagged with 'new' by Spotify (to my knowledge this means albums released within the last week).
- Adding the albums and their information to a local MongoDB to keep a track of which albums have and have not been submitted (as well as which social media networks their links have been submitted to).
- Posting a link to the "http://open.spotify" link of the album on integrated social networks with additional information formatted and included where available. Additional information includes album popularity and available regions, as well as upcoming concerts for the artist if they have record of them on Songkick. 

Requirements
--------------
In order to make this script work as it does, it relies on the following utilities and their respective dependencies:
- urllib2
- simplejson
- pymongo
- praw
- pytumblr
- twython
- python-songkick

Limitations
--------------
- At the moment, Twitter is limiting the account status' to 160 per day. This isn't great considering there's a backlog of links to submit to Twitter in my database, and Spotify could tag more than 160 albums as new per day. A potential workaround would be to only submit links to Twitter of artists who have say more than 5,000 followers but currently in the lookup API there's no way to get the number of follwers an artist has. 
- Whenever the script runs, it's just submitting link after link 10 seconds apart. So if you're following the Tumblr or Twitter account, it's just going to keep spamming your feed until the script is done. I may be able to set up a queue system with Tumblr and I'm not worried that much about Reddit, but again Twitter may be an issue. 
- Integration with the Songkick API has started (yay!) but it's doing an API lookup for both Reddit and Tumblr posts seperately, meaning there's two lookups being made instead of potentially one. The Songkick Developer T&C don't allow storage of the gig information, so I made need to do some rewriting of the script instead of looking at saving gig details to MongoDB.
- It's just running on my laptop at the moment, with a local database. Ideally, I'd like to move the automated script and database onto a linux server somewhere and keep it running every 6 hours. 
- There probably is more... I just have to think of them.

Updates
--------------
- 23 Oct 2013 - Fixes, script now goes through the first 5 pages of the API results (that should be enough... right?)
- 25 Oct 2013 - Fixes, script now submits to its very own Tumblr blog - newonpsotify.tumblr.com!
- 27 Oct 2013 - Fixes (all day every day), script now submits to its very own Twitter account - @_newonspotify!
- 8 Nov 2013 - Fixes, "Random" and "About" pages added to Tumblr blog, new logo for sub-reddit, Songkick API integration for Tumblr and Reddit posts, Tiny.cc API integration to create shorter links in Twitter posts

Plans for the future
--------------
- LastFM API integration (what could be useful here? similar artists?)
- Pinterest as the next social service?
- List reviews of album, linking to sources potentially?
- Facebook API integration to search for verified Artist pages to determine like count
- A pot of gold at the end of the rainbow
- Whatever suggestions come my way