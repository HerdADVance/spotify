from django.db import models
from myauth.models import CustomUser

class Podcast(models.Model):
	spotify_id = models.CharField(max_length=100, unique=True)
	name = models.CharField(max_length=200)
	image = models.CharField(max_length=200, null=True)
	publisher = models.CharField(max_length=200, null=True)
	users = models.ManyToManyField(CustomUser, related_name='podcasts') 
	
	def clean(self):
		super().clean()
		
		# Prevent player from being owned in a league more than once
		# if Roster.objects.filter(league_id=self.league_id, player_id=self.player_id).exists():
		# 	raise ValidationError("Player already owned by a team in this league")

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)