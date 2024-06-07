from django.http import JsonResponse
from django.shortcuts import render
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException
from .util import *
from core.util import *
from core.models import SearchAttempt


# =========== Get newest episodes for each of user's followed shows ===========
@redirect_if(no_spotify_token)
def get_new_episodes(request, data):

	# Front end data (number of episodes to get per show and list of shows followed)
	num_episodes = request.POST.get('num_episodes') or 10
	shows = json.loads(request.POST.get('shows'))

	# Return error if no shows
	if not shows:
		return send_error("You have no shows to get new episodes for. Please add shows to your follow list and try again.", 400)

	# Check our DB to see if user hasn't exceeded API call limits, return error if has
	ip_address = request.META.get('REMOTE_ADDR')
	allowed_to_send = check_api_access_limits(ip_address, 'new-episodes')
	if not allowed_to_send:
		return send_error("You have exceeded your hourly limit for getting new episodes. Please wait until later to try again.", 400)

	# Save new search attempt to DB or send error
	saved_attempt = save_search_attempt(ip_address, 'new-episodes')
	if not saved_attempt:
		return send_error('There was a problem with our database. Please try again later.', 400)

	# Spotify Token brought in through decorator
	token = data['token']['access_token']
	sp = spotipy.Spotify(auth=token)

	# Empty list to be filled and returned to front end
	episodes = []

	# Loop through each show
	for show in shows:

		# Attempt to get most recent Episodes for each Show iteration from API
		try:
			episodes_result = sp.show_episodes(show['id'], limit=num_episodes)['items']
		except Exception as error:
			return send_error('There was a problem retrieving your episodes. Please try again.', 400)

		# Loop through each Episode and append to list
		for episode in episodes_result:
			episodes.append({
				'name': episode['name'],
				'podcast_name': show['name'],
				'podcast_uri': show['uri'],
				'podcast_id': show['id'],
				'release_date': episode['release_date'],
				'duration': format_duration(episode['duration_ms']),
				'uri': episode['uri'],
				'image': show['image']
			})

	# Sort Episodes by date and format dates
	episodes = sorted(episodes, key=lambda x: x['release_date'], reverse=True)
	episodes = format_dates(episodes)

	# Return Episodes to front end
	return JsonResponse({'episodes': json.dumps(episodes)}, safe=False)



# =========== Get User's Followed Shows and Episodes ===========
@redirect_if(no_spotify_token)
def get_shows_and_episodes(request, data):

	# Number of episodes from front end
	num_episodes = request.POST.get('num_episodes') or 10

	# Check our DB to see if user hasn't exceeded API call limits, return error if has
	ip_address = request.META.get('REMOTE_ADDR')
	allowed_to_send = check_api_access_limits(ip_address, 'shows-episodes')
	if not allowed_to_send:
		return send_error("You have exceeded your hourly limit for searching shows & episodes. Please wait until later to try again.", 400)

	# Save new search attempt to DB or send error
	saved_attempt = save_search_attempt(ip_address, 'shows-episodes')
	if not saved_attempt:
		return send_error('There was a problem with our database. Please try again later.', 400)

	# Spotify Token brought in through decorator
	token = data['token']['access_token']
	sp = spotipy.Spotify(auth=token)

	# Empty lists to be filled and returned to front end
	shows = []
	episodes = []

	# Attempt to get followed shows from Spotify API
	try:
		shows_result = sp.current_user_saved_shows(limit=30, offset=0, market='US')
	except Exception as error:
		return send_error('There was a problem retrieving your followed shows. Please try again.', 400)

	# Loop through followed shows 
	for item in shows_result['items']:
		show = item['show']

		# Append each show to Shows list
		shows.append({
			'id': show['id'],
			'name': show['name'],
			'uri': show['uri'],
			'image': show['images'][1]['url']
		})

		# Attempt to get Episodes for each Show iteration
		try: 
			episodes_result = sp.show_episodes(show['id'], limit=num_episodes)['items']
		except Exception as error:
			return send_error('There was a problem retrieving your followed episodes. Please try again.', 400)

		# Loop through episodes for each show
		for episode in episodes_result:

			# Append each episode to Episodes list
			episodes.append({
				'name': episode['name'],
				'podcast_name': show['name'],
				'podcast_uri': show['uri'],
				'podcast_id': show['id'],
				'release_date': episode['release_date'],
				'duration': format_duration(episode['duration_ms']),
				'uri': episode['uri'],
				'image': show['images'][1]['url']
			})

	# Sort and format Shows and Episodes
	shows = sorted(shows, key=lambda x: x['name'])
	episodes = sorted(episodes, key=lambda x: x['release_date'], reverse=True)
	episodes = format_dates(episodes)

	# Return Shows and Episodes to front end
	return JsonResponse({'shows': json.dumps(shows), 'episodes': json.dumps(episodes)}, safe=False)



# =========== Get show results for user's search ==========
@redirect_if(no_spotify_token)
def get_searched_shows(request, data):

	# Return error if search query somehow blank (also checked on frontend)
	search_query = request.POST.get('query')
	if not search_query:
		return send_error("You didn't submit a search query. Please try again.", 400)

	# Check our DB to see if user hasn't exceeded API call limits, return error if has
	ip_address = request.META.get('REMOTE_ADDR')
	allowed_to_send = check_api_access_limits(ip_address, 'search-shows')
	if not allowed_to_send:
		return send_error("You have exceeded your hourly limit for searching shows. Please wait until later to try again.", 400)

	# Spotify Token brought in through decorator 
	token = data['token']['access_token']
	sp = spotipy.Spotify(auth=token)

	# Save new search attempt to DB or send error
	saved_attempt = save_search_attempt(ip_address, 'search-shows', search_query)
	if not saved_attempt:
		return send_error('There was a problem with our database. Please try again later.', 400)

	# Attempt to get searched shows result from Spotify API
	try:
		result = sp.search(search_query, limit=10, type='show', market='US')
	except Exception as error:
		return send_error('There was a problem searching for shows. Please try again.', 400)

	# Empty list of searched shows to fill and return to front end
	shows = []

	# Loop through shows returned from API
	for show in result['shows']['items']:
		
		# Append Show to list
		shows.append({
			'name': show['name'],
			'description': show['description'],
			'html_description': show['html_description'],
			'uri': show['uri'],
			'image': show['images'][1]['url'],
			'num_episodes': show['total_episodes'],
			'id': show['id']
		})

	# Return searched shows to front end
	return JsonResponse({'shows': json.dumps(shows)}, safe=False)



# ========== Add or remove a show from the user's follow list ==========
@redirect_if(no_spotify_token)
def add_remove_show(request, data):

	# Front end data (show to add/remove, action type)
	show_id = request.POST.get('show_id')
	action = request.POST.get('action')

	# Return error if no show ID
	if not show_id:
		return send_error("You didn't select a show to add. Please try again.", 400)

	# Check our DB to see if user hasn't exceeded API call limits, return error if has
	ip_address = request.META.get('REMOTE_ADDR')
	allowed_to_send = check_api_access_limits(ip_address, 'add-remove-shows')
	if not allowed_to_send:
		return send_error("You have exceeded your hourly limit for adding or removing shows. Please wait until later to try again.", 400)

	# Spotify Token brought in through decorator
	token = data['token']['access_token']
	sp = spotipy.Spotify(auth=token)

	# Save new search attempt to DB or send error
	saved_attempt = save_search_attempt(ip_address, 'add-remove-show', show_id)
	if not saved_attempt:
		return send_error('There was a problem with our database. Please try again later.', 400)

	# Use the Spotify API to remove or add a show (or return error message if fails)
	if action == 'remove':
		try:
			result = sp.current_user_saved_shows_delete(shows=[show_id])
		except Exception as error:
			return send_error('There was a problem adding that show. Please try again.', 400)
	else:
		try: 
			result = sp.current_user_saved_shows_add(shows=[show_id])
		except Exception as error:
			return send_error('There was a problem deleting that show. Please try again.', 400)
		

	# Return success message and action type to front end
	success = ''
	return JsonResponse({'success': success, 'action': action}, safe=False)
	


# ========== Get the user's Spotify display name ==========
@redirect_if(no_spotify_token)
def get_user_display_name(request, data):

	# Check our DB to see if user hasn't exceeded API call limits, return error if has
	ip_address = request.META.get('REMOTE_ADDR')
	allowed_to_send = check_api_access_limits(ip_address, 'display-name')
	if not allowed_to_send:
		return send_error("You have exceeded your API limit. Please wait until later to try again.", 400)
	
	# Spotify Token brought in through decorator
	token = data['token']['access_token']
	sp = spotipy.Spotify(auth=token['access_token'])

	# Save new search attempt to DB or send error
	saved_attempt = save_search_attempt(ip_address, 'display-name')
	if not saved_attempt:
		return send_error('There was a problem with our database. Please try again later.', 400)
	
	# Use the Spotify API to get the current user's display name
	try:
		result = sp.current_user()
	except Exception as error:
		return send_error('There was a problem getting your Spotify display name. Please try again.', 400)

	# Return the user's display name to the front end
	return result['display_name']



