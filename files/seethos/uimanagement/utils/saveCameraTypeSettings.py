from usermanagement.models import Users
from usermanagement.utils.hash import encryption, decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime
from uimanagement.models import CameraFeeds, CameraSettings,Alarms


def func_saveCameraTypeSettings(request_data, token):
	try:
		response = {}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response["message"] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			try:
				alarm = Alarms.objects.get(alarmUid=request_data["alarmUid"])
			except:
				response["message"] = "Incorrect alarm Id"
				response["statuscode"] = 400
				return response			
			try:
				cam_obj = CameraSettings.objects.get(camType=request_data["camType"])
				cam_obj.rectColours = str(request_data["rectColours"])
				cam_obj.alarm=alarm
				cam_obj.save()
			except:				
				cam_obj = CameraSettings(
					camType=request_data["camType"],
					alarm=alarm,
					rectColours=str(request_data["rectColours"]),
				)
				cam_obj.save()
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
