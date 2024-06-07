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
  - login_user
  - logout_user
  - register_user
  - splash
  - spotify_auth
  - spotify_callback
------------------
'''


#==== Attempts to login user or return errors
def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username').lower()
		password = request.POST.get('password')
 
		# Find the user or return user not found error
		try:
			user = CustomUser.objects.get(username=username)
		except:
			messages.error(request, 'User does not exist')
			return redirect_to_login()

		# Authenticate the user or return Incorrect password error
		user = authenticate(request, username=username, password=password)
		if not user:
			messages.error(request, 'Incorrect password')
			return redirect_to_login()

		# User authenticated so log them in and redirect to home
		login(request, user)
		return redirect('home')

	# Unauthorized GET redirects to splash page login form 
	else:
		return redirect_to_login()



#==== Logs out user
def logout_user(request):
	logout(request)
	return redirect_to_login()



#==== Attempts to register user or return errors
def register_user(request):
	if request.method == 'POST':

		# Attempt to validate registration for a new user 
		form = RegistrationForm(request.POST)

		# If new user is valid, create user, log them in, redirect to Lobby
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('lobby')

		# New user not valid, redirect to register form and return errors
		else:
			for field, errors in form.errors.items():
				print(form.errors.as_json())
				for error in errors:
					messages.error(request, get_custom_error_message(error))
			return redirect('splash')
			
	# Unauthorized GET redirects to splash page registration form
	else:
		redirect('splash')



#==== Splash page that doubles as Spotify login page
def splash(request):

	# Get random splash image
	image = get_splash_image()

	context = {
		'splash': True,
		'image': image,
	}

	return render(request, 'splash.html', context)


#==== Send user to spotify to login with their credentials
def spotify_auth(request):

	sp_oauth = SpotifyOAuth(
		client_id = os.getenv('SPOTIFY_API_CLIENT_ID'),
		client_secret = os.getenv('SPOTIFY_API_CLIENT_SECRET'),
		redirect_uri = request.build_absolute_uri(reverse('spotify-callback')),
		scope = 'user-library-read user-library-modify user-read-private user-read-email user-read-playback-state',
	)

	auth_url = sp_oauth.get_authorize_url()
	return HttpResponseRedirect(auth_url)



#==== Bring the user back after logging in through Spotify
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


