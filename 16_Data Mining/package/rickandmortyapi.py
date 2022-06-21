# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from botocore.vendored.six import b
import requests
import pandas as pd

base_url="https://rickandmortyapi.com/api/"
character_url=base_url+"character/"
location_url=base_url+"location/"
episode_url=base_url+"episode/"

class Base():
	def api_info():
		return requests.get(base_url).json()
		
	def schema():
		temp=requests.get(character_url).json()
		return temp['info'].keys()


class Character():

	def get_all():
		return requests.get(character_url).json()

	def get_page(number):
		return requests.get(character_url+'?page='+str(number)).json()

	def get(id=None):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return requests.get(character_url+str(id)).json()

	def filter(**kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=character_url+"?"+query_url
		return requests.get(final_url).json()

	def schema():
		temp=requests.get(character_url).json()
		return temp['results'][0].keys()

class Location():

	def get_all():
		return requests.get(location_url).json()

	def get(id=None):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return requests.get(location_url+str(id)).json()

	def filter(**kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=location_url+'?'+query_url
		return requests.get(final_url).json()

	def schema():
		temp=requests.get(location_url).json()
		return temp['results'][0].keys()


class Episode():

	def get_all():
		a = pd.DataFrame(requests.get("https://rickandmortyapi.com/api/episode/?page=1").json()['results'])
		b = pd.DataFrame(requests.get("https://rickandmortyapi.com/api/episode/?page=2").json()['results'])
		c = pd.DataFrame(requests.get("https://rickandmortyapi.com/api/episode/?page=3").json()['results'])

		base = pd.concat([a,b,c])

		return base

	def get(id=None):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return requests.get(episode_url+str(id)).json()

	def filter(**kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=episode_url+'?'+query_url
		return requests.get(final_url).json()

	def schema():
		temp=requests.get(episode_url).json()
		return temp['results'][0].keys()
    
def extract_character(start_page = 1, end_pages = 5):
    
    db_characters = []
    
    try:
        for page in range(start_page,end_pages):
            db = pd.DataFrame(Character.get_page(page)["results"])
            db["page"] = page
            db_characters.append(db)
    except :
            db = pd.DataFrame([1,2,3,4,5,6,7,8,9,10,11,12])
            db["page"] = page
            db_characters.append(db)
            
    return pd.concat(db_characters)
