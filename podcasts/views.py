
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth



def spotify_authh(request):
	# Set up the Spotify OAuth parameters
	client_id = '62b6f46750c3430d8d9f58b5f93de781'
	client_secret = 'a9357d18918248089eae34a7064bb972'
	redirect_uri = request.build_absolute_uri(reverse('spotify_callback'))
	scope = 'user-library-read user-read-private user-read-email user-read-playback-state'

	# Create the Spotify OAuth object
	sp_oauth = SpotifyOAuth(
	    client_id=client_id,
	    client_secret=client_secret,
	    redirect_uri=redirect_uri,
	    scope=scope
	)

	# Check if the user has already authorized the app
	token_info = sp_oauth.get_cached_token()
	token_info = None
	if token_info:

		# Use the cached token to create the Spotify client
		sp = spotipy.Spotify(auth=token_info['access_token'])
		result = sp.current_user_saved_shows(limit=30, offset=0, market='US')

		# Append each show into shows list
		shows = []
		for item in result['items']:
			show = item['show']
			shows.append({
				'name': show['name'],
				'description': show['description'],
				'html_description': show['html_description'],
				'uri': show['uri'],
				'image': show['images'][1]['url'],
				'num_episodes': show['total_episodes'],
				'id': show['id']
			})
		shows = sorted(shows, key=lambda x: x['name'])

		context = {'shows': shows}
		return render(request, 'search/results.html', context)

		#current_user_saved_shows_add(shows=[])

	else:
		# If the user hasn't authorized the app, redirect to the Spotify authorization page
		auth_url = sp_oauth.get_authorize_url()
		return HttpResponseRedirect(auth_url)

def spotify_callbackk(request):
	"""
	Callback view to handle the Spotify authorization response.
	"""
	# Get the authorization code from the Spotify response
	code = request.GET.get('code')
	if code:
		# Use the authorization code to get an access token
		client_id = '62b6f46750c3430d8d9f58b5f93de781'
		client_secret = 'a9357d18918248089eae34a7064bb972'
		redirect_uri = request.build_absolute_uri(reverse('spotify-callbackk'))
		scope = 'user-library-read user-read-private user-read-email user-read-playback-state'

		sp_oauth = SpotifyOAuth(
			client_id=client_id,
			client_secret=client_secret,
			redirect_uri=redirect_uri,
			scope=scope
		)

		token_info = sp_oauth.get_access_token(code, check_cache=False)

		# Create the Spotify client with the access token
		sp = spotipy.Spotify(auth=token_info['access_token'])
		# Perform actions with the Spotify client
		#user_profile = sp.current_user()

		result = sp.current_user_saved_shows(limit=30, offset=0, market='US')

		#return HttpResponse(f"Hello, {user_profile['display_name']}!")
		return HttpResponse(f"Hello, {result}!")
	else:
		return HttpResponse(f"Error: {code}")








def index(request):
	# cid = '62b6f46750c3430d8d9f58b5f93de781'
	# secret = 'a9357d18918248089eae34a7064bb972'
	# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
	# redirect_uri = "http://localhost:8000/podcasts/"
	# scope = "user-read-private user-read-email"

	# sp_oauth = SpotifyOAuth(
	#     client_id=cid,
	#     client_secret=secret,
	#     redirect_uri=redirect_uri,
	#     scope=scope
	# )

	# token_info = sp_oauth.get_access_token()
	# access_token = token_info['access_token']

	# sp = spotipy.Spotify(auth=access_token)

	# result = sp.current_user_saved_shows(limit=30, offset=0, market='US')
	# print('PRINTING RESULTS================')
	# print(result)
	
	return render(request, 'search/index.html')


def search(request):
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


def add(request):
	podcast_uri = request.POST.get('uri')
	print(podcast_uri)
	return render(request, 'search/index.html')