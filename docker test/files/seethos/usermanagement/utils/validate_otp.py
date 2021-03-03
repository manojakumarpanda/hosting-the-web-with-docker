import logging
import os
import re
import sys
import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from usermanagement.models import AccessManagement, Users
from usermanagement.utils.hash import decryption, encryption

refresh_lockout = getattr(settings, "LOCKOUT_COUNT_RESET_DURATION", None)
time_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)



def func_validate_otp(request_data):
	try:
		response={}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}

		curr_user = Users.objects.filter(id=request_data['user_id'])
		otp=request_data["otp"]
		if len(curr_user) > 0:
			curr_user = curr_user[0]
			email=curr_user.email
			curr_access = AccessManagement.objects.filter(name=curr_user)
			if len(curr_access) > 0:
				curr_access = curr_access[0]
			else:
				logs["data"]["status_message"] = "User Access for email {} does not exists in the database.".format(email)
				logs["data"]["data_fields"] = [email]
				response["message"] = "User Access for email {} does not exists in the database.".format(email)
				response["statuscode"] = 400
				logs["added_at"] = datetime.utcnow()
				actvity_logs.insert_one(logs)
				return response
		else:
			logs["data"]["status_message"] = "User With this id {} does not exists in the database.".format(request_data['user_id'])
			logs["data"]["data_fields"] = [email]
			response["message"] = "User With this id {} does not exists in the database.".format(request_data['user_id'])
			response["statuscode"] = 400
			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response

		# Check if OTP has been initiated
		if curr_access.otp is None:
			""" 
			Check if OTP request was initiated 
			""" 
			logs["data"]["status_message"] = "No OTP has been initiated for email ID {}.".format(email)
			logs["data"]["data_fields"] = [email]
			response["message"] = "No OTP has been initiated for email ID {}.".format(email)
			response["statuscode"] = 400
			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response

		# Check if OTP hasn't expired
		if timezone.now() > curr_access.otp_expiry_time:
			curr_access.last_otp_attempt = None
			curr_access.otp = None
			curr_access.otp_attempts = 0
			curr_access.otp_expiry_time = None
			curr_access.save()      
			
			logs["data"]["status_message"] = "OTP expired for email ID {}.".format(email)
			logs["data"]["data_fields"] = [email]
			response["message"] = "OTP expired for email ID {}.".format(email)
			response["statuscode"] = 400

			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response
				
		"""
		Check if account isnt locked for access
		1. If password attempts count is equal 'count_threshold' and user tried to login again within 'time_threshold' mins of last attempt then freeze the account
		2. Password attempts count is reset everytime user correctly logs in
		3. Password attempts count is incremented every time an wrong passwor is entered within 'time_threshold' minutes of last password attempt
		"""
		if curr_access.otp_attempts>=count_threshold:
			if timezone.now() < curr_access.last_otp_attempt + timedelta(minutes=refresh_lockout) and curr_access.otp_attempts == count_threshold:
				logs["data"]["status_message"] = "Multiple invalid OTP attempts for email ID {}. Please try after sometime.".format(email)
				logs["data"]["data_fields"] = [email]
				response["message"] = "Multiple invalid OTP attempts for email ID {}. Please try after sometime.".format(email)
				response["statuscode"] = 400
				logs["added_at"] = datetime.utcnow()
				actvity_logs.insert_one(logs)
				return response
			elif timezone.now() >= curr_access.last_otp_attempt + timedelta(minutes=refresh_lockout) and curr_access.otp_attempts == count_threshold:
				"""
				Reset counters after lockout period is expired. Flow does not break here.
				"""
				curr_access.last_otp_attempt = None
				curr_access.otp_attempts = 0
				curr_access.save()
		                   
		"""
		last_otp_attempt is set to None when correct password request is received
		"""
		logging.info("curr_access.otp ==>{} == encryption(str(otp))==>{}=={}".format(curr_access.otp,encryption(str(otp)),otp))
		if curr_access.otp == encryption(str(otp)):                  
			token=curr_user.token
			curr_access.last_otp_attempt = None
			curr_access.otp_attempts = 0
			curr_access.otp = None
			curr_access.otp_expiry_time = None
			curr_access.save()

			logs["data"]["status_message"] = "Otp Verified changed successfully for email ID {}.".format(email)
			logs["data"]["data_fields"] = [email]

			response["message"] = "Otp Verified successfully."
			response["statuscode"] = 200
			response["token"] = token

			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response
		else:
			"""
			last_otp_attempt is set only when the first wrong password request is received
			"""
			if curr_access.last_otp_attempt is None:
				curr_access.last_otp_attempt = timezone.now()
				curr_access.otp_attempts += 1
				curr_access.save()    
				logs["data"]["status_message"] = "Incorrect OTP for email ID {}.".format(email)
				logs["data"]["data_fields"] = [email]
				logging.info('Incorrect OTP1')
				response["message"] = "Incorrect OTP."
				response["statuscode"] = 400

				logs["added_at"] = datetime.utcnow()
				actvity_logs.insert_one(logs)
				return response
             
			elif timezone.now() < curr_access.last_otp_attempt + timedelta(minutes=time_threshold):
				if curr_access.otp_attempts == count_threshold - 1: #This will help add a lockout delta to last login attempt
					curr_access.last_otp_attempt = timezone.now()
				curr_access.otp_attempts = curr_access.otp_attempts + 1
				curr_access.save()

				logs["data"]["status_message"] = "Incorrect OTP for email ID {}.".format(email)
				logs["data"]["data_fields"] = [email]
				response["message"] = "Incorrect OTP."
				logging.info('Incorrect OTP2')
				response["statuscode"] = 400
				logs["added_at"] = datetime.utcnow()
				actvity_logs.insert_one(logs)
				return response
         
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.info(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + " " + str(e))
		error_logs.insert_one({
			"error_type": str(exc_type),
			"file_name": str(fname),
			"line_no": str(exc_tb.tb_lineno),
			"error": str(e)
		})
		response["statuscode"] = 500
		return response	
