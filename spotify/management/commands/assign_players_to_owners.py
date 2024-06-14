from django.core.management.base import BaseCommand
from players.models import Player#, PlayerOwnership
from teams.models import Team, Roster
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


		Roster.objects.all().delete()

		for player in players:
			if player['fields']['team_id']:
				db_player = Player.objects.get(rapidapi_id=str(player['fields']['rapidapi_id']))
				db_team = Team.objects.get(id=player['fields']['team_id'])

				new_row = Roster()
				new_row.player_id = db_player.id
				new_row.team_id = db_team.id
				new_row.league_id = db_team.league.id
				new_row.save()

			
		

		
			