from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import shutil

class Command(BaseCommand):
	help = 'Delete the DB, PyCache and Migration files, and make and run migrations'

	def handle(self, *args, **options):

		# Delete the DB file
		os.remove('./db.sqlite3')

		# Delete the PyCache folders
		shutil.rmtree('./myauth/__pycache__')
		#shutil.rmtree('./core/__pycache__')
		#shutil.rmtree('./search/__pycache__')

		# Delete migrations folder
		shutil.rmtree('./myauth/migrations')
		#shutil.rmtree('./core/migrations')
		#shutil.rmtree('./search/migrations')

		# Make and run migrations
		call_command('makemigrations', 'myauth')
		#call_command('makemigrations', 'core')
		#call_command('makemigrations', 'search')
		call_command('migrate')

		# Add fixtures
		call_command('create_users')


