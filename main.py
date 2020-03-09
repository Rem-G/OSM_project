from folium_ex import *
from tweepy_ex import *

import tweepy
import webbrowser
import os


def twitter_listenner_call(limit = 1000):
	stream_listener = StreamListener(limit = limit)
	stream = tweepy.Stream(auth=api.auth, listener = stream_listener)

	user_request = input("Track keyword/locations 0/1 : ")
	if user_request == '1':
		stream.filter(locations=[5.69915771484375, 45.14524196975275, 5.7808685302734375, 45.194619099094645])
	
	elif user_request == '0':
		stream.filter(track=["coronavirus", "Coronavirus", "Macron", "macron"], languages=["fr", "en"])

def folium_compile(coordinates, polygon = [], stopwords = False):
	OSM = OpenStreetMap(coordinates = coordinates, zoom = 5, tiles = 'Stamen Toner', polygon = polygon)
	OSM.json_data(stopwords = stopwords)
	OSM.export()

def main():
	print("##############################")
	print("(!) To change tweepy track parameters, please change these directly in main.py (!)")
	user_request_tweepy = input("Do you want to track new tweets ? y/n : ")

	if user_request_tweepy == "y":
		limit = int(input("How many tweets ? : "))
		twitter_listenner_call(limit = limit)

	print("##############################")

	user_request_folium = input("Do you want to display the 10 most tweeted words in Grenoble/display tweets in the city they come ? y/n : ")

	if user_request_folium == "y":
		#10 most tweeted words in Grenoble
		folium_compile(
			stopwords = True,
			coordinates = [48.856614, 2.3522219],
			polygon =
				[
					[
					  45.15976909839157,
					  5.71014404296875
					],
					[
					  45.15976909839157,
					  5.74310302734375
					  
					],
					[
					  45.18736044117691,
					  5.74310302734375
					],
					[
					  45.18736044117691,
					  5.71014404296875
					],
					[
					  45.15976909839157,
					  5.71014404296875
					]
				]


		)
	else:
		#Basic display, display tweets in the city they were sent
		folium_compile(coordinates = [48.856614, 2.3522219])

	webbrowser.open(os.getcwd()+"/index.html", 2)


main()


	

