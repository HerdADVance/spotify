from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from .util import *


@redirect_if(no_spotify_token)
def home(request, data):

	scrape = False
	shows_file = 'data/shows.json'
	episodes_file = 'data/episodes.json'
	
	if scrape:

		#if(data['logging_in'])
		token = data['token']['access_token']

		# Use the cached token to create the Spotify client
		sp = spotipy.Spotify(auth=token)
		result = sp.current_user_saved_shows(limit=30, offset=0, market='US')

		# Lists that we'll pass to the template
		shows = []
		episodes = []

		# Loop through shows
		for item in result['items']:
			show = item['show']
			
			# Append show info to shows list
			shows.append({
				'name': show['name'],
				'description': show['description'],
				'html_description': show['html_description'],
				'uri': show['uri'],
				'image': show['images'][1]['url'],
				'num_episodes': show['total_episodes'],
				'id': show['id'],
			})

			# API call for show's episodes
			show_episodes = sp.show_episodes(show['id'], limit=8)['items']

			# Append episode info to episodes list
			for episode in show_episodes:
				episodes.append({
					'name': episode['name'],
					'podcast_name': show['name'],
					'podcast_uri': show['uri'],
					'release_date': episode['release_date'],
					'duration': format_duration(episode['duration_ms']),
					'uri': episode['uri'],
					'image': show['images'][1]['url'],
				})

		# Sort shows by name and episodes by most recent release date
		shows = sorted(shows, key=lambda x: x['name'])
		episodes = sorted(episodes, key=lambda x: x['release_date'], reverse=True)

		# Format dates in episodes
		episodes = format_dates(episodes)

		# Save shows and episodes as JSON
		with open(shows_file, 'w') as f:
			json.dump(shows, f)
		with open(episodes_file, 'w') as f:
			json.dump(episodes, f)


	# Not scraping so read JSON files for shows and episodes
	else:
		with open(shows_file, 'r') as json_file:
			shows = json.load(json_file)
		with open(episodes_file, 'r') as json_file:
			episodes = json.load(json_file)



	context = {'shows': shows, 'episodes': episodes}
	return render(request, 'core/home.html', context)


