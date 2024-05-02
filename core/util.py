
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

# Decorator function used on every page to redirect to splash page for Spotify login
def redirect_if(condition_func):
	def decorator(view_func):
		@wraps(view_func)
		def wrapper(request, *args, **kwargs):
			token = condition_func(request)
			if not token:
				return redirect('splash')
			data = {
				'token': token
			}
			return view_func(request, data=data, *args, **kwargs)
		return wrapper
	return decorator


# Condition function for above decorator that checks Spotify auth
def no_spotify_token(request):
	sp_oauth = SpotifyOAuth(
		client_id = os.getenv('SPOTIFY_API_CLIENT_ID'),
		client_secret = os.getenv('SPOTIFY_API_CLIENT_SECRET'),
		redirect_uri = request.build_absolute_uri(reverse('spotify-callback')),
		scope = 'user-library-read user-read-private user-read-email user-read-playback-state',
	)
	
	#return None
	return sp_oauth.get_cached_token()


def format_dates(episodes):
	for episode in episodes:
		episode['release_date'] = datetime.strptime(episode['release_date'], "%Y-%m-%d").strftime("%-m/%d/%y")
	return episodes

def format_duration(ms):
	return int(round((ms / 1000 / 60), 0))
