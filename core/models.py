from django.db import models

# Create your models here.
class SearchAttempt(models.Model):
	spotify_username = models.CharField(max_length=100)
	ip_address = models.CharField(max_length=100)
	search_type = models.CharField(max_length=20)
	search_query = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name