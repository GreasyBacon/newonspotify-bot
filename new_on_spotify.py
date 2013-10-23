import time
import pymongo
import urllib2
import simplejson
import praw

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
	search = collection.find_one({	"artist":artist,
									"album": album
								})
	return search

def submit_new_link(post):
	title = post["artist"] + " - " + post["album"] 
	
	#submit new link for album
	try:
		submission = bot.submit('newonspotify', title, url=post["album_link"], raise_captcha_exception=True)
		print "Submitted link for " + title 
	except:
		print "Album already submitted on sub-reddit."
		return

	try: 
		#creating links for comment
		album = "[" + post["album"] + "](" + post["album_link"] + ")"
		artist = "[" + post["artist"] + "](" + post["artist_link"] + ")"
		
		#submit comment with additional information
		comment =  'Additional Information\n\n* Album Name - ' + album + '\n\n* Album Popularity - ' + post["popularity"] + '\n\n* Artist Name - ' + artist + '\n\n* Available Territories - ' + post["availableterritories"]
		
		#add additional information as a comment to submission
		submission.add_comment(comment)
		print "submitted comment for " + title
	except:
		print "Comment could not be submitted."
		return

def update_album_status(album, artist):
	search_request = search_for_album(album, artist)
	if search_request is None: 
		print "I'm not submitting this album, there's no record in the db."
	else:
		try:
			collection.update({'_id':search_request["_id"]}, {'$set':{"status":"submitted"}})
		except:
			print "Database record NOT updated for " + album + ". Something went wrong?"
		else:
			print "Database record updated for " + album

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
								"status" : "to be submitted" 
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
	#newonspotify_bot
	#ilovespotify
	counter = 0
	global bot
	bot = praw.Reddit(	'Link Submitter for /r/newonspotify using PRAW'
						'Created by: /u/GreasyBacon'
						'Contact: dilutedthoughts@outlook.com' )	
	bot.login("username", "password")

	posts_to_submit = collection.find({"status": "to be submitted"})

	for post in posts_to_submit:
 		submit_new_link(post)
 		update_album_status(post["album"], post["artist"])
 		counter = counter + 1
	 	time.sleep(10) #make sure not to exceed API limits

	print str(counter) + " submissions of new albums to /r/newonspotify."

if __name__ == "__main__":
	pages = [5,4,3,2,1]
	try:
		connect_to_mongo()
		for page in pages:
			albums = get_api_data(page)
			insert_into_database(albums)
			post_to_reddit()
	except: 
		print "Something has gone wrong. Probably a good idea to investigate."