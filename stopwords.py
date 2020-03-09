import json

from nltk.tokenize import word_tokenize 
import nltk

class StopWords():
	def __init__(self, data):
		self.data = data

	def extract_words(self, text):
		"""
		:param text str: Text to analyse
		:return text_tokenyze_final list: Text without stopwords
		"""
		stopwords_list = list()
		languages = ['french', 'english']

		for language in languages:
			with open('stop_words/{}.txt'.format(language), 'r') as data:
				lines = data.readlines()

				for element in lines:
					stopwords_list.append(element[:len(element)-1])

		text_tokenize = word_tokenize(text)#Split the words
		text_tokenize_final = list()

		for word in text_tokenize:
			if word.lower() not in stopwords_list:
				text_tokenize_final.append(word)

		return text_tokenize_final

	def open_data(self):
		words = list()

		for element in self.data:
			extracted_words = self.extract_words(element['text'])
			for word in extracted_words:
				words.append(word)

		return words

	def sort_data(self):
		"""
		Sort words by frequence and return the 10 first elements
		"""
		words = self.open_data()
		dict_frequence_words = dict()
		cpt = 0

		most_frequente_words = dict()

		for word in words:
			if word not in dict_frequence_words:
				dict_frequence_words[word] = 0
			else:
				dict_frequence_words[word] += 1

		sorted_dict = sorted(dict_frequence_words.items(), key = lambda x: x[1])[::-1]

		return sorted_dict[:10]