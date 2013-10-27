import time
import pymongo
import urllib2
import simplejson
import praw
import pytumblr
from twython import Twython

#setting up mongodb connection	
def connect_to_mongo():
	client = pymongo.MongoClient()
	db = client.newonspotify
	global collection
	collection = db.albums

#calling spotify API
def get_api_data(page):
	if page == 1:
		url = "http://ws.spotify.com/search/1/album.json?q=tag:new"
	else:
		url = "http://ws.spotify.com/search/1/album.json?q=tag:new&page=" + str(page)
	request = urllib2.urlopen(url)
	json_response = simplejson.loads(request.read())
	album_data = json_response["albums"]
	print "Getting data for page " + str(page)
	return album_data

#search for an album in the database
def search_for_album(album, artist):
	search = collection.find_one({"artist":artist, "album": album})
	return search

def submit_new_twitter_link(post):
	if len(post["album"].split(" ")) == 1:
		album = "#" + post["album"]
	else:
		album = post["album"] 
	
	if len(post["artist"].split(" ")) == 1:
		artist = "#" + post["artist"]
	else:
		artist = post["artist"]

	status = album + " by " + artist + " - " + post["album_link"]

	try:
		twitter_bot.update_status(status=status.encode('utf-8'))
	except:
		print "Submission for twitter status went wrong."
		return False
	else:
		print post["album"] + " submitted to @_newonspotify."
		return True

def submit_new_tumblr_link(post):
	embed_html = "<b>Album Information</b><br><ul><li><i>Album</i> - <a href=" + post["album_link"] + ">" + post["album"] + "</a><li><i>Album Popularity</i> - " + post["popularity"] + "<li><i>Artist</i> - <a href=" + post["artist_link"] + ">" + post["artist"] + "</a><li><i>Available Territories</i> - " + post["availableterritories"] + "</ul>"

	artist = post["artist"]
	album = post["album"]
	#submit new link for album
	try:
		submission = tumblr_bot.create_audio('newonspotify', caption=embed_html.encode('utf-8'), external_url=post["album_link"], tags=[artist.encode('utf-8'), album.encode('utf-8'), "spotify", "music", "newonspotify"])
	except:
		print "Submission for tumblr went wrong."
		return False
	else:
		print post["album"] + " submitted to newonspotify.tumblr.com."
		return True

def submit_new_reddit_link(post):
	title = post["artist"] + " - " + post["album"] 
	
	#submit new link for album
	try:
		submission = reddit_bot.submit('newonspotify', title, url=post["album_link"], raise_captcha_exception=True)
		print "Submitted link for " + title 
	except:
		print "Album already submitted on sub-reddit."
		return "already_submitted"

	try: 
		#creating links for comment
		album = "[" + post["album"] + "](" + post["album_link"] + ")"
		artist = "[" + post["artist"] + "](" + post["artist_link"] + ")"
		
		#submit comment with additional information
		comment =  'Additional Information\n\n* Album Name - ' + album + '\n\n* Album Popularity - ' + post["popularity"] + '\n\n* Artist Name - ' + artist + '\n\n* Available Territories - ' + post["availableterritories"]
		
		#add additional information as a comment to submission
		submission.add_comment(comment)
		print "submitted comment for " + title
		return True
	except:
		print "Comment could not be submitted."
		return False

def update_album_status(platform, album, artist):
	search_request = search_for_album(album, artist)
	if search_request is None: 
		print "I'm not submitting this album, there's no record in the db."
	else:
		try:
			collection.update({'_id':search_request["_id"]}, {'$set':{platform:"submitted"}})
		except:
			print "Database record NOT updated for " + album + ". Something went wrong?"
		else:
			print "Database record updated for " + album + " on platform " + platform

def convert_spotify_link(href):
	artist_check = "artist"
	if artist_check in href:
		new_href = href.replace("spotify:artist:", "http://open.spotify.com/artist/")
	else:
		new_href = href.replace("spotify:album:", "http://open.spotify.com/album/")
	return new_href

#insert new albums into database
def insert_into_database(album_data):
	counter = 0
	
	for albums in album_data:
		search_attempt = search_for_album(albums["name"], albums["artists"][0]["name"])

		if search_attempt is None:
			try:
				album_link = convert_spotify_link(albums["href"])
				artist_link = convert_spotify_link(albums["artists"][0]["href"])
				mongo_album = { "album" : albums["name"],
								"album_link" : album_link,
								"popularity" : albums["popularity"],
								"artist" : albums["artists"][0]["name"],
								"artist_link": artist_link,
								"availableterritories" : albums["availability"]["territories"], 
								"tumblr" : "to be submitted",
								"reddit" : "to be submitted",
								"twitter" : "to be submitted"
							}
				collection.insert(mongo_album)
				print albums["name"] + " by " + albums["artists"][0]["name"] + " added to database."
				counter = counter + 1
			except: 
				print albums["name"] + " not added for some reason - check it out"
		else:
			print albums["name"] + " already in database"

	print str(counter) + " albums added to Database."

def post_to_reddit():
	#posting to /r/newonspotify
	counter = 0
	global reddit_bot
	reddit_bot = praw.Reddit('Link Submitter for /r/newonspotify using PRAW'
							'Created by: /u/GreasyBacon'
							'Contact: dilutedthoughts@outlook.com' )	
	reddit_bot.login("username", "password")

	posts_to_submit = collection.find({"reddit" : "to be submitted"})

	for post in posts_to_submit:
 		response = submit_new_reddit_link(post)
 		if (response is True) or (response is "already_submitted"):
 			update_album_status("reddit", post["album"], post["artist"])
 			counter = counter + 1
	 		time.sleep(10)

	print str(counter) + " submissions of new albums to /r/newonspotify."

def post_to_tumblr():
	#posting to newonspotify.tumblr.com
	counter = 0
	global tumblr_bot
	tumblr_bot = pytumblr.TumblrRestClient(
	'<consumer_key>',
	'<consumer_secret>',
	'<oauth_token>',
	'<oauth_secret>'
	)

	try:
		tumblr_bot.info()
	except:
		print "Issue with tumblr log-in credentials."
	else:
		posts_to_submit = collection.find({"tumblr" : "to be submitted"})

		for post in posts_to_submit:
			response = submit_new_tumblr_link(post)
			if response is True:
				update_album_status("tumblr", post["album"], post["artist"])
				counter = counter + 1
				time.sleep(10)

		print str(counter) + " submissions of new albums to newonspotify.tumblr.com"

def post_to_twitter():
	#posting to @_newonspotify
	counter = 0
	app_key = 'app_key'
	app_secret = 'app_secret'
	oauth_token =  'oauth_token'
	oauth_token_secret = 'oauth_token_secret'

	try:
		global twitter_bot
		twitter_bot = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
		twitter_bot.verify_credentials()
	except:
		print "Issue with twitter log in credentials."
	else:
		posts_to_submit = collection.find({"twitter" : "to be submmitted"})
		# will eventually need to change to:
		# posts_to_submit = collection.find({"twitter" : "to be submitted"})

		for post in posts_to_submit:
			response = submit_new_twitter_link(post)
			if response is True:
				update_album_status("twitter", post["album"], post["artist"])
				counter = counter + 1
				time.sleep(10)

		print str(counter) + " submissions of new albums to @_newonspotify twitter"

def songkick_integration():
	#adding nearest songkick concerts
	print "should soon be working"

if __name__ == "__main__":
	pages = [10,9,8,7,6,5,4,3,2,1]
	try:
		connect_to_mongo()
		for page in pages:
			albums = get_api_data(page)
			insert_into_database(albums)
			post_to_reddit()
			post_to_tumblr()
			post_to_twitter()
	except: 
		print "Something has gone wrong. Probably a good idea to investigate."