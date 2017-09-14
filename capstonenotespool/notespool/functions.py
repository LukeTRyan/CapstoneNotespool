import re
import string
import random
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

def email_verification(email):
	if re.search(r'(@connect.qut.edu.au)', email):
		return True
	else:
		return False

def id_generator(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))