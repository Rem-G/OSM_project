# Import the necessary package to process data in JSON format
import sys
sys.path.append('E:/bureau/ISOC/Lib/site-packages/tweepy')

# Import the tweepy library
import tweepy
from tweepy.auth import OAuthHandler
import json

from sql import *

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '1225316531170693120-OU4eonbuowe1ODI0Wv7twh6NCsWJqP'
ACCESS_SECRET = 'Pgkqc6wsWrx5XxshDTADouECcVmbXae4bYxG8EK3iRZEi'
CONSUMER_KEY = 'CDmTa7prcly0VkLY9XSAsfb2b'
CONSUMER_SECRET = 'zc8sz1AYSuxkmLlizPN7Q3crmUlZ2W9YWnyAtqdc1n86M3wPU3'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False, compression=False)

class StreamListener(tweepy.StreamListener):
	def __init__(self, limit):
		self.limit = limit
		self.file_name = 'data.json'
		self.cpt = 0
		super(StreamListener, self).__init__()

	def on_status(self, status):
		if self.cpt < self.limit:
			if status._json['place']:
				self.cpt += 1
				print(status._json['place']['name'])

				SQL().insert_into_db(status._json['text'], status._json['place']['bounding_box']['coordinates'][0])

				with open('data.json', 'r') as json_file:
					data = json.load(json_file)

				data.append(status._json)

				with open('data.json', 'w') as json_file:
					json.dump(data, json_file, indent = 3)
		else:
			return False

	def on_error(self, status_code):
		if status_code == 420:
			return False




