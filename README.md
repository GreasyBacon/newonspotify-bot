Bot for /r/newonspotify
==============

Introduction
--------------
I decided to sign up to GitHub to host the code for my first bot written in Python for my subreddit - /r/newonspotify. 

That's it really :)

Purpose
--------------
The purpose of the bot is to act as an auto-submitter of links to new albums released on Spotify for users subscribed to the sub-reddit. 


How it works
--------------
It works in three stages:
- Accessing the Spotify 'lookup' API for albums tagged with 'new' by Spotify (to my knowledge this means albums released within the last week)
- Adding the albums and their information to a local MongoDB to keep a track of which albums have and have not been submitted.
- Posting a link to the "http://open.spotify" link of the album on /r/newonspotify with additional information provided in the comments by the bot.

Plans for the future
--------------
- Better title submissions
- A pot of gold at the end of the rainbow
- Whatever suggestions come my way