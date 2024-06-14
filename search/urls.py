
from django.urls import path, include
from .views import *

urlpatterns = [
    path('search/', index),
    path('search-podcast', search_podcast, name="search-podcast"),
    path('add-podcast', add_podcast, name="add-podcast"),
]
