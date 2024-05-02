
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
	path('welcome/', splash, name="splash"),
	path('spotify_auth', spotify_auth, name="spotify-auth"),
	path('spotify_callback', spotify_callback, name="spotify-callback"),
	path('login/', login_user, name="login_user"),
	path('logout/', logout_user, name="logout_user"),
	path('register/', register_user, name="register_user"),
]
