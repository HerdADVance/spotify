
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
	class Meta:
		model = CustomUser
		fields = ["username", "password"]
		# error_messages = {
		# }


class RegistrationForm(UserCreationForm):
	#email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ["username", "email", "password1", "password2"]
		error_messages = {
			'username': {
				'unique': "Username already taken",
				'max_length': "Username too long. 30 chars max"
			},
			'email': {
				'unique': "Account with this e-mail address already exists",
				'invalid': "E-mail address invalid"
			}
		}