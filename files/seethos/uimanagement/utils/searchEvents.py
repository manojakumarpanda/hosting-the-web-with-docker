from usermanagement.models import Users
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
from django.db import IntegrityError
import re
import ast
import os
import sys
import logging
import datetime
from uimanagement.models import Events
from dateutil.parser import parse
import parsedatetime as ps
cal = ps.Calendar()

def func_searchEvents(request_data, token):
	try:
		response={}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response['message'] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			if request_data.get("camId","") != "":
				if request_data.get("period",None) is None:
					# events = Events.objects.filter(camFeedId=request_data["camId"],eventTime=request_data["camType"],eventTime__gte=parse(request_data["fromDate"]),eventTime__lte=parse(request_data["toDate"]))
					time_struct, parse_status = cal.parse(request_data["fromDate"])
					from_date = datetime.datetime(*time_struct[:6])
					if parse_status != 1:
						response['message'] = 'Invalid search parameters'
						response["statuscode"] = 400
						return response							
					time_struct, parse_status = cal.parse(request_data["toDate"])
					if parse_status != 1:
						response['message'] = 'Invalid search parameters'
						response["statuscode"] = 400
						return response						
					to_date = datetime.datetime(*time_struct[:6])	
					logging.info(from_date)
					logging.info(to_date)
					events = Events.objects.filter(camFeedId=request_data["camId"],eventTime__range=((from_date,to_date)))
				else:
					time_struct, parse_status = cal.parse(request_data["period"])
					if parse_status == 1:
						period = datetime.datetime(*time_struct[:6])
						from_date = period
						to_date = datetime.datetime.now()
						logging.info(from_date)
						logging.info(to_date)
						logging.info(type(from_date))
						# events = Events.objects.filter(camFeedId=request_data["camId"],eventTime__gte=datetime.datetime.now()-period,eventTime__lte=datetime.datetime.now())
						events = Events.objects.filter(camFeedId=request_data["camId"],eventTime__range=((from_date,to_date)))
						logging.info("Q@#")
					else:
						response['message'] = 'Invalid search parameters'
						response["statuscode"] = 400
						return response						
				ret_data = []	
				for 	event in events:
					eventDetails = {}
					eventDetails["eventUid"]=event.eventUid
					eventDetails["camId"]=event.camFeedId
					eventDetails["timeStamp"]=event.eventTime
					eventDetails["objects"]=ast.literal_eval(event.objsDetected)
					eventDetails["videoPath"]=event.videoPath
					ret_data.append(eventDetails)
				response["data"] = ret_data
				response["statuscode"] = 200
				return response
			else:
				response['message'] = 'Invalid search parameters'
				response["statuscode"] = 400
				return response
	except Exception as e:
		# exc_type, exc_obj, exc_tb = sys.exc_info()
		# fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# logging.info(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + " " + str(e))
		logging.info(e)
		response['message'] = 'There was some error'
		response["statuscode"] = 400
		return response
