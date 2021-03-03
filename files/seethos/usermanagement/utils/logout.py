from usermanagement.models import Users
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
import os,sys,logging
import datetime

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_logout(request_data, token):
	try:
		response = {}
		# email=request_data['email']
		curr_user = Users.objects.filter(token=token)

		if len(curr_user) == 0:
			response['message'] = "Invalid token."
			response["statuscode"] = 400
			return response
		else:
			curr_user = curr_user[0]
			curr_user.token = ""
			curr_user.save()
		response['message'] = "User logged out successfully."
		response["statuscode"] = 200
		
		return response			
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		logging.info("Login API error2-> "+str(e) + " " + str(exc_tb.tb_lineno))
		response['message']='The username or password is not correct'
		response["statuscode"]=400
		return response