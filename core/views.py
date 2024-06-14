from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from .util import *


@redirect_if(no_spotify_token)
def home(request, data):

	# If first time coming from Spotify login, get username that will be cached in LocalStorage
	if request.GET.get('login_redirect'):
		token = data['token']['access_token']
		sp = spotipy.Spotify(auth=token)
		result = sp.current_user()
		display_name = result['display_name']
	else:
		display_name = ''

	# We go directly to the front end and rely on LocalStorage
	context = {'display_name': display_name}
	return render(request, 'core/home.html', context)



