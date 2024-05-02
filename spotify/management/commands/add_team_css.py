from django.core.management.base import BaseCommand
import csv
import json

class Command(BaseCommand):
	help = 'Create CSS with colors for each team'

	def handle(self, *args, **options):

		filepath = 'data/nfl_teams.csv'

		css_output = ''
		with open(filepath, encoding='utf-8') as csv_file_handler:
			csv_reader = csv.DictReader(csv_file_handler)
			for row in csv_reader:
				css_output += '.' + row['slug'] + '{background: ' + row['pri'] + '; color: ' + row['sec'] + ';}' + '\n'

		print(css_output)
				