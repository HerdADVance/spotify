from django.shortcuts import redirect
import random


# Would rather do this forms.py but can't get codes for password errors to work
def get_custom_error_message(error):
	errors = {
		"The two password fields didn’t match.": "Passwords don't match",
		"This password is too short. It must contain at least 8 characters.": "Password too short. 8 character minimum",
		"The password is too similar to the username.": "Password too similar to username",
		"This password is too common.": "Password too common",
	}

	return errors[error] if error in errors else error
	

# Return a random image for the splash page 
def get_splash_image():
	images = [
		'splash.jpeg',
	]

	random.shuffle(images)
	return images[0]


# For when the login form should be shown on the splash page instead of the registration form
def redirect_to_login():
	response = redirect('splash')
	response['Location'] += '?form=login'
	return response
