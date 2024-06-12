
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('new-episodes', get_new_episodes, name='new-episodes'),
    path('show-episodes', get_show_episodes, name='show-episodes'),
    path('shows-episodes', get_shows_and_episodes, name='shows-episodes'),
    path('search-shows', get_searched_shows, name='search-shows'),
    path('add-show', add_remove_show, name='add-remove-show'),
]
