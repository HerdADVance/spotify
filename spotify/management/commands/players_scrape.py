
from django.core.management.base import BaseCommand
from core.models import CollegeTeam, NFLTeam, Position
from players.models import Player
import json
import requests


class Command(BaseCommand):
	help = 'Scrape players data using RapidAPI'


	def add_arguments(self, parser):
		parser.add_argument('scrape', type=bool)

	def handle(self, *args, **options):

		filepath = 'players/fixtures/rapidapi-scrape.json'
		url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerList"
		headers = {
			"X-RapidAPI-Key": "b4bae12909msh0f8689be0ad64ffp169837jsnfba8c7da5caa",
			"X-RapidAPI-Host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
		}


		# SCRAPE API for new file
		# if options['scrape']:
		# 	response = requests.get(url, headers=headers)
		# 	response_dict = response.json()
		# 	response_json = json.dumps(response_dict)
		# 	with open(filepath, 'w') as file:
		# 		file.write(response_json)
		# 	return # end of Scrape



		# READ existing file
		with open(filepath, 'r') as json_file:
			players = json.load(json_file)['body']

		print('reading')

		positions = ['QB', 'FB', 'RB', 'WR', 'TE']
		teams = []
		colleges = []

		pid = 1
		for player in players:
			
			if player['pos'] not in positions:
				continue

			if player['team'] not in teams:
				teams.append(player['team'])
				new_team = NFLTeam()
				new_team.slug = player['team']
				new_team.save()
				nfl_team = new_team
			else:
				nfl_team = NFLTeam.objects.get(slug=player['team'])

			if player['isFreeAgent'] == 'True':
				nfl_team = None

			if player['school'] not in colleges:
				colleges.append(player['school'])
				new_college = CollegeTeam()
				new_college.name = player['school']
				new_college.save()
				college_team = new_college
			else:
				college_team = CollegeTeam.objects.get(name=player['school'])


			if 'lastGamePlayed' in player:
				last_game_played = player['lastGamePlayed']
			else:
				last_game_played = None
				
		
			position_slug = 'RB' if player['pos'] == 'FB' else player['pos']
			position = Position.objects.get(slug=position_slug)

			new_player = Player()
			#new_player.id = pid
			new_player.position = position
			new_player.nfl_team = nfl_team
			new_player.college_team = college_team
			new_player.name = player['longName']
			new_player.height = player['height']
			new_player.weight = player['weight']
			new_player.age = player['age']
			new_player.birthday = player['bDay']
			new_player.experience = player['exp']
			new_player.last_game = last_game_played
			new_player.jersey_number = player['jerseyNum']
			new_player.cbs_id = player.get('cbsPlayerID', None)
			new_player.espn_id = player.get('espnID', None)
			new_player.espn_id_full = player.get('espnIDFull', None)
			new_player.fp_id = player.get('fantasyProsPlayerID', None)
			new_player.rapidapi_id = player.get('playerID', None)
			new_player.rotowire_id = player.get('rotoWirePlayerID', None)
			new_player.sleeper_id = player.get('sleeperBotID', None)
			new_player.yahoo_id = player.get('yahooPlayerID', None)
			new_player.save()

			#pid += 1
		




