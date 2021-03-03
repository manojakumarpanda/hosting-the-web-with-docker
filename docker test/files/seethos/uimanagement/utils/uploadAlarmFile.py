from usermanagement.models import Users
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime
from uimanagement.models import Alarms

def func_uploadAlarmFile(request_data, token):
	try:
		response={}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response['message'] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			try:
				if request_data.get("alarmUid",0) == 0:
					# Create a new row in db
					try:
						file_obj = request_data["file"]
						Alarms.objects.create(alarmName=request_data["alarmName"],originalFileName=str(file_obj),datafile=file_obj)
						response["statuscode"] = 200
						return response						
					except IntegrityError:
						response['message'] = 'Duplicate Alarm Name'
						response["statuscode"] = 400
						return response					
					except Exception as e:
						logging.info(str("3"))					
						logging.info(str(e))
						response['message'] = 'There was some error'
						response["statuscode"] = 400
						return response
				else:
					# Modify existing record
					try:
						file_obj = request_data["file"]
						alarm = 	Alarms.objects.get(alarmUid=request_data["alarmUid"])
						alarm.alarmName = request_data["alarmName"]
						alarm.originalFileName=str(file_obj)
						alarm.datafile=file_obj
						alarm.save()
						response["statuscode"] = 200
						return response
					except IntegrityError:
						response['message'] = 'Duplicate Alarm Name'
						response["statuscode"] = 400
						return response
					except Exception as e:
						logging.info(str("1"))
						logging.info(str(e))
						response['message'] = 'There was some error'
						response["statuscode"] = 400
						return response		
			except Exception as e:
				logging.info(str("2"))
				logging.info(str(e))
				response['message'] = 'There was some error'
				response["statuscode"] = 400
				return response
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.info(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + " " + str(e))
		response['message'] = 'There was some error'
		response["statuscode"] = 400
		return response