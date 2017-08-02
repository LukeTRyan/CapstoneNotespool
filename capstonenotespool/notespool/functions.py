import re
from django.contrib.auth.models import User

def password_verification(password):

	count = 0
    
	if re.search(r'\d', password):
		count += 1
	if re.search(r'[A-Z]', password):
		count += 1
	if re.search(r'[a-z]', password):
		count += 1

	if count == 3:
		return True
	else:
		return False