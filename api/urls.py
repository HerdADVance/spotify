
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('new-episodes', get_new_episodes, name='new-episodes'),
    path('show-episodes', get_show_episodes, name='show-episodes'),
    path('get-all-followed', get_all_followed, name='get-all-followed'),
    path('search-playlists', get_searched_playlists, name='search-playlists'),
    path('search-shows', get_searched_shows, name='search-shows'),
    path('add-show', add_remove_show, name='add-remove-show'),
]
