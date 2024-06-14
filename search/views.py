
from django.shortcuts import render
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def index(request):
	return render(request, 'search/index.html')


def search_podcast(request):
	cid = '62b6f46750c3430d8d9f58b5f93de781'
	secret = 'a9357d18918248089eae34a7064bb972'
	client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
	sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

	query = request.POST.get('search-query')
	result = sp.search(query, limit=1, type='show', market='US')
	shows = []

	for show in result['shows']['items']:

		for key, value in show.items():
			print(f"{key}: {value}")
		
		shows.append({
			'name': show['name'],
			'description': show['description'],
			'html_description': show['html_description'],
			'uri': show['uri'],
			'image': show['images'][1]['url'],
			'num_episodes': show['total_episodes'],
			'id': show['id']
		})

	#shows = json.dumps(shows)
	context = {'shows': shows}

	
	return render(request, 'search/results.html', context)


def add_podcast(request):
	podcast_uri = request.POST.get('uri')
	print(podcast_uri)
	return render(request, 'search/index.html')