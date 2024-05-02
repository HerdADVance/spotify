from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('search', search, name="search-podcast"),
    path('add', add, name="add-podcast"),
    path('spotify_authh', spotify_authh, name="spotify_authh"),
    path('spotify_callbackk', spotify_callbackk, name="spotify_callbackk"),
]

#https://accounts.spotify.com/authorize?scope=user-read-private+user-read-email&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fpodcasts%2Fspotify_callback&client_id=62b6f46750c3430d8d9f58b5f93de781&flow_ctx=b1e5fceb-1050-462c-8c19-dc531445ec99%3A1713346268