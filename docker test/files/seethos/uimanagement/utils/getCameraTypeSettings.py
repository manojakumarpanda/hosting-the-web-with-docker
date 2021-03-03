from usermanagement.models import Users
from usermanagement.utils.hash import encryption, decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import ast
import logging
import datetime
from uimanagement.models import CameraFeeds, CameraSettings,Alarms


def func_getCameraTypeSettings(request_data, token):
	try:
		response = {}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response["message"] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			try:
				cam_objs = CameraSettings.objects.all()
				ret_obj = []
				for cam in cam_objs:
					temp_obj = {}
					temp_obj["camType"] = cam.camType
					temp_obj["alarmType"] = cam.alarm.alarmUid
					temp_obj["rectColours"] = ast.literal_eval(cam.rectColours)
					ret_obj.append(temp_obj)
				response["data"] = ret_obj
			except Exception as e:
				logging.info(e)
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