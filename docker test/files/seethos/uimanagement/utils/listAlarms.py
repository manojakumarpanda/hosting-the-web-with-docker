from usermanagement.models import Users
from usermanagement.utils.hash import encryption, decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime
from uimanagement.models import Alarms
media_url = getattr(settings, "MEDIA_URL", None)

def func_listAlarms(request_data, token):
	try:
		response = {}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response["message"] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			try:
				alarms = Alarms.objects.all()
				ret_obj = []
				for alarm in alarms:
					temp_obj = {}
					temp_obj["alarmUid"] = alarm.alarmUid
					temp_obj["alarmName"] = alarm.alarmName
					temp_obj["url"] = media_url + str(alarm.datafile)
					ret_obj.append(temp_obj)
				response["data"] = ret_obj
			except:
				response["data"] = []
			response["statuscode"] = 200
			return response
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.info(
			str(exc_type)
			+ " "
			+ str(fname)
			+ " "
			+ str(exc_tb.tb_lineno)
			+ " "
			+ str(e)
		)
		response["message"] = "There was some error"
		response["statuscode"] = 400
		return response