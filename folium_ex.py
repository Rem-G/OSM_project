import folium
import json
import requests

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from stopwords import *

class OpenStreetMap:
	def __init__(self, coordinates, zoom, polygon, tiles='Stamen Terrain'):
		self.cities = list()
		self.polygon = polygon
		self.osm_map = folium.Map(
			location = coordinates,
			zoom_start = zoom,
			tiles = tiles,

			# tiles : 'Stamen Toner', 'Stamen Terrain'
		)

	def get_city_center(self, coordinates):
		"""
		:param coordinates list : lat long
		:return list : lat long, city center of coordinates
		"""
		data = requests.get('https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}'.format(coordinates[0], coordinates[1]))
		data_json = data.json()
		if 'error' in data_json.keys():
			return None
		return [float(data_json['lat']), float(data_json['lon'])]
	
	def coor_in_polygon(self, coordinates, polygon):
		"""
		:param coordinates list: lat long
		:param polygon dict : polygon of a city
		:return bool: coordinates in the polygon
		"""
		point = Point(coordinates)
		polygon = Polygon(polygon)
		return polygon.contains(point)

	def avg_coordinates(self, coordinates):
		"""
		;param coordinates list : long lat
		:return list : lat long, average coordinates of the twitter polygon
		"""
		sum_lat = sum_long = 0
		
		for coord in coordinates:
			sum_lat += float(coord[1])
			sum_long += float(coord[0])

		return [sum_lat/len(coordinates), sum_long/len(coordinates)]

	def add_layers(self, geojson_data, text=""):
		"""
		Add layers on the folium map
		:param geojson_data dict: polygon to add on the map
		:param text list: data to display on the map
		"""
		geojson = folium.GeoJson(geojson_data).add_to(self.osm_map)

		if len(self.polygon):
			popup = folium.Popup('10 most tweeted words :\n' + text, max_width=450)
		else:
			popup = folium.Popup(text, max_width=450)

		popup.add_to(geojson)
		geojson.add_to(self.osm_map)

	def get_osm_geometry(self, coordinates):
		"""
		:param coordinates list: lat long
		:return None or dict: If coordinates are in a city/town/suburb/village/hamlet reeturn geometry else return None
		"""
		data = requests.get('https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}'.format(coordinates[0], coordinates[1]))
		data_json = data.json()
		address_elements = data_json['address'].keys()
		place = None

		if 'city' in address_elements: place = data_json['address']['city']
		elif 'town' in address_elements: place = data_json['address']['town']
		elif 'suburb' in address_elements: place = data_json['address']['suburb']
		elif 'village' in address_elements: place = data_json['address']['village']
		elif 'hamlet' in address_elements: place = data_json['address']['hamlet']

		if place and place not in self.cities:
			self.cities.append(place)
			country = data_json['address']['country']
			url = "https://nominatim.openstreetmap.org/search?city={}&country={}&polygon_geojson=1&format=json".format(place, country)
			data = requests.get(url)
			print(url)
			try:
				data_json = data.json()[0]
				if len(data_json['geojson']['coordinates'][0]) > 2:#The polygon is not a point
					return data_json['geojson']
			except:
				pass

		return None

	def extract_data_polygon(self, data):
		"""
		Keeps only tweets sent from our research polygon
		:param data list: All tweets
		:return data list: Sorted data
		"""
		cpt = 0
		delete = False
		data_polygon = list()

		for tweet in data:
			if tweet['place']['place_type'] == 'city':
				coor = self.get_city_center(self.avg_coordinates(tweet['place']['bounding_box']['coordinates'][0]))

				if self.coor_in_polygon(coor, self.polygon):
					data_polygon.append(tweet)
				else:
					cpt += 1
					print(cpt, "tweets out of research area")
			else:
				cpt += 1
				print(cpt, "tweets out of research area")		

		return data_polygon


	def json_data(self, stopwords = False):
		"""
		Main function of the class, coordinates all elements
		:param stopwords Bool: Indicate if the program has to display the most frequent words or single tweets
		"""
		with open('data.json', 'r') as json_file:
			data = json.load(json_file)

		if len(self.polygon):
			data = self.extract_data_polygon(data)

		cpt = 0
		cities = list()
		stopword_text = str()

		if stopwords:
			stopword_text = str(StopWords(data).sort_data())

		for tweet in data:
			print('Tweet {}/{}'.format(cpt, len(data)-1))

			if tweet['place']['place_type'] == 'city' and tweet['place']['name'] not in cities:
				cities.append(tweet['place']['name'])
				coor = self.get_city_center(self.avg_coordinates(tweet['place']['bounding_box']['coordinates'][0]))
				geojson = self.get_osm_geometry(coor)

				if geojson:#Check if the city is not already in the layers
					if stopwords:
						self.add_layers(geojson, stopword_text)
					else:
						self.add_layers(geojson, tweet['text'])
					print('DONE \n')
			cpt += 1

	def export(self, name="index.html"):
		self.osm_map.save(name)
