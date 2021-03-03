from django.conf import settings
superuser = getattr(settings, "SUPERUSER", None)
superuser_pass = getattr(settings, "SUPERUSERPASS", None)

def run_config(email):
	if email == superuser:
		pass
	return	