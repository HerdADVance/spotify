from django.core.management.base import BaseCommand
from draft.models import Draft, DraftPick
from leagues.models import League
from teams.models import Team
import csv
import json

class Command(BaseCommand):
	help = 'Create CSS with colors for each team'

	def handle(self, *args, **options):

		filepath = 'data/picks.csv'

		league = League.objects.get(id=1)
		new_draft = Draft.objects.create(
			league = league,
			year = 2024
		)
		new_draft.save()

		with open(filepath, encoding='utf-8') as csv_file_handler:
			csv_reader = csv.DictReader(csv_file_handler)
			draft_round = 1
			for row in csv_reader:
				for idx, cell in row.items():

					team = Team.objects.get(id=cell)

					new_pick = DraftPick.objects.create(
						draft = new_draft,
						team = team,
						round_number = draft_round,
						pick_number = idx,
					)
					new_pick.save()
				draft_round += 1
				