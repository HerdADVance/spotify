from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from .forms import CustomLoginForm, RegistrationForm
from .models import CustomUser
from .util import *
from core.util import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from django.http import HttpResponseRedirect, HttpResponse

 
'''
VIEWS IN THIS FILE
------------------
  - splash
  - spotify_auth
  - spotify_callback
------------------
'''


# Splash page that doubles as Spotify login page
# ----------------------------------------------
def splash(request):

	# Get random splash image
	image = get_splash_image()

	context = {
		'splash': True,
		'image': image,
	}

	return render(request, 'splash.html', context)




# Send user to spotify to login with their credentials
# ----------------------------------------------------
def spotify_auth(request):

	sp_oauth = SpotifyOAuth(
		client_id = os.getenv('SPOTIFY_API_CLIENT_ID'),
		client_secret = os.getenv('SPOTIFY_API_CLIENT_SECRET'),
		redirect_uri = request.build_absolute_uri(reverse('spotify-callback')),
		scope = 'user-library-read user-library-modify user-read-private user-read-email user-read-playback-state',
	)

	auth_url = sp_oauth.get_authorize_url()
	return HttpResponseRedirect(auth_url)




# Bring the user back after logging in through Spotify
# -----------------------------------------------------
def spotify_callback(request):
	code = request.GET.get('code')
	if code:

		sp_oauth = SpotifyOAuth(
			client_id = os.getenv('SPOTIFY_API_CLIENT_ID'),
			client_secret = os.getenv('SPOTIFY_API_CLIENT_SECRET'),
			redirect_uri = request.build_absolute_uri(reverse('spotify-callback')),
			scope = 'user-library-read user-library-modify user-read-private user-read-email user-read-playback-state',
		)
		
		token = sp_oauth.get_access_token(code)		

		return redirect('/?login_redirect=True')


