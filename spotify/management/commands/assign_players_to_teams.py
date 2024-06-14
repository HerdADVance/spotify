from django.core.management.base import BaseCommand
from players.models import Player
from bs4 import BeautifulSoup
import json
import requests

class Command(BaseCommand):
	help = 'Add players to dynasty teams based off rosters in April 2024'

	def handle(self, *args, **options):

		# Options
		json_filepath = 'players/fixtures/player.json'

		# Read saved file
		with open(json_filepath, 'r') as json_file:
			players = json.load(json_file)


		# Add players to teams
		for player in players:
			if player['fields']['team_id']:
				db_player = Player.objects.get(rapidapi_id=str(player['fields']['rapidapi_id']))
				db_player.team_id = player['fields']['team_id']
				db_player.save()

			
		

		
			