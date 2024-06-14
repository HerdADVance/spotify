from django.core.management.base import BaseCommand
from players.models import Player
from bs4 import BeautifulSoup
import json
import requests

class Command(BaseCommand):
	help = 'Scrape Fantasy Pros to get dynasty rankings'

	def add_arguments(self, parser):
		parser.add_argument('scrape', type=bool)

	def handle(self, *args, **options):

		# Options
		json_filepath = 'players/fixtures/fantasypros-scrape.json'
		url = 'https://www.fantasypros.com/nfl/rankings/dynasty-overall.php'

		# Scrape FantasyPros for new file
		# if(options['scrape'] == True):
		# 	print('scraping')
		# 	response = requests.get(url, verify=True)
		# 	soup = BeautifulSoup(response.text, 'html.parser')
		# 	json_str = response.text.split('var ecrData')[1].split('var sosData')[0]
		# 	with open(json_filepath, 'w') as file:
		# 		file.write(json_str)
		# 	return
		

		# Read saved file
		with open(json_filepath, 'r') as json_file:
			players = json.load(json_file)['players']


		# Save FP overall and position ranks for each player
		for player in players:
			try:
				db_player = Player.objects.get(fp_id=str(player['player_id']))
			except:
				continue
				
			db_player.fp_dyn_ovr_rank = int(player['rank_ecr'])
			db_player.fp_dyn_pos_rank = int(player['pos_rank'][2:])
			db_player.save()
		

		return
		

		
			