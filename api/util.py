from django.http import JsonResponse
from core.models import SearchAttempt
from django.utils import timezone
from datetime import timedelta


# ----- See if user hasn't used the API too much recently (based on their IP) -----
def check_api_access_limits(ip_address, search_type):

	# Get number of attempts for this type of API call in the last hour 
	one_hour_ago = timezone.now() - timedelta(hours=1)
	num_attempts = SearchAttempt.objects.filter(ip_address=ip_address, search_type=search_type, created_at__gte=one_hour_ago).count()
	
	api_call_types = {
		'add-remove-shows': 5,
		'display-name': 5,
		'new-episodes': 5,
		'search-shows': 5,
		'shows-episodes': 5,
	}

	return True if num_attempts < api_call_types[search_type] else False
	


# ----- Save user's search attempt (or other type of API call) to DB -----
def save_search_attempt(ip_address, search_type, search_query=''):

	# Prepare new Search Atttempt
	new_search_attempt = SearchAttempt.objects.create(
		ip_address = ip_address,
		search_type = search_type,
		search_query = search_query
	)

	# Attempt to save to DB, return T/F
	try:
		new_search_attempt.save()
	except Exception as error:
		return False
	return True
	


# ----- Handle return of error to front end -----
def send_error(msg, code):
	return JsonResponse({'error': msg }, status=code)