from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from myauth.models import CustomUser
import json

class Command(BaseCommand):
	help = 'Create users from JSON fixture in myauth'

	def handle(self, *args, **options):

		filepath = 'myauth/fixtures/custom_user.json'
		with open(filepath, 'r') as json_file:
			users = json.load(json_file)

		for user in users:

			hashed_password = make_password(user['fields']['password'])
			new_user = CustomUser.objects.create(
				username=user['fields']['username'],
				password=hashed_password,
				email=user['fields']['email'],
				first_name=user['fields']['first_name'],
				last_name=user['fields']['last_name'],
				is_superuser=1 if user['fields']['username'] == 'alex' else 0
			)
			new_user.save()