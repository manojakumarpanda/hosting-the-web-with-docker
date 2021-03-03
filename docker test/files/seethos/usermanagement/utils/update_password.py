from usermanagement.models import Users,AccessManagement
from django.shortcuts import render
from usermanagement.utils.hash import encryption,decryption
from datetime import datetime, timedelta
from django.utils import timezone
import uuid
import logging,re,os,sys
from django.conf import settings
refresh_lockout = getattr(settings, "LOCKOUT_COUNT_RESET_DURATION", None)
time_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)

def check_password(password):
	space_condn = 1 if password.find(" ") < 0 else 0
	upper_case_condn = 0 if not re.search("[A-Z]", password) else 1 
	lower_case_condn = 0 if not re.search("[a-z]", password) else 1 
	number_case_condn = 0 if not re.search("[0-9]", password) else 1 
	special_character_condn = 0 if not re.search("[\W]", password) else 1 
	length_condn = 0 if len(password) < 15 else 1
	return all([space_condn, upper_case_condn, lower_case_condn, number_case_condn, special_character_condn, length_condn])


def generate_hash():
	return uuid.uuid4().hex

def func_update_password(request_data):
	try:
		response={}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}

		email = request_data['email'].lower()
		otp = request_data['otp'] #OTP
		new_password = request_data['new_password']

		curr_user = Users.objects.filter(email=email)
		if len(curr_user) > 0:
			curr_user = curr_user[0]
			curr_access = AccessManagement.objects.filter(name=curr_user)
			if len(curr_access) > 0:
				curr_access = curr_access[0]
			else:
				logs["data"]["status_message"] = "User Access for email {} does not exists in the database.".format(email)
				logs["data"]["data_fields"] = [email]
				response["message"] = "User Access for email {} does not exists in the database.".format(email)
				response["statuscode"] = 500

				logs["added_at"] = datetime.utcnow()
				actvity_logs.insert_one(logs)
				return response
		else:
			logs["data"]["status_message"] = "Email ID {} does not exists in the database.".format(email)
			logs["data"]["data_fields"] = [email]
			response["message"] = "Email ID {} does not exists in the database.".format(email)
			response["statuscode"] = 500

			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response

		# Check the criteria of password
		if not check_password(new_password):
			logs["data"]["status_message"] = "Password entered for email ID {} does not meet the conditions.".format(email)
			logs["data"]["data_fields"] = [email]
			response["message"] = "Password entered for email ID {} does not meet the conditions.".format(email)
			response["statuscode"] = 500

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
			response["statuscode"] = 500

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
			response["statuscode"] = 500

			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response
				
		"""
		Check if account isnt locked for access
		1. If password attempts count is equal 'count_threshold' and user tried to login again within 'time_threshold' mins of last attempt then freeze the account
		2. Password attempts count is reset everytime user correctly logs in
		3. Password attempts count is incremented every time an wrong passwor is entered within 'time_threshold' minutes of last password attempt
		"""
		if curr_access.last_otp_attempt is not None:
			if timezone.now() < curr_access.last_otp_attempt + timedelta(minutes=refresh_lockout) and curr_access.otp_attempts == count_threshold:
				logs["data"]["status_message"] = "Multiple invalid OTP attempts for email ID {}. Please try after sometime.".format(email)
				logs["data"]["data_fields"] = [email]

				response["message"] = "Multiple invalid OTP attempts for email ID {}. Please try after sometime.".format(email)
				response["statuscode"] = 500
				
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
		# try:                    
		"""
		last_otp_attempt is set to None when correct password request is received
		"""
		if curr_access.otp == encryption(str(otp)):                  
			token = generate_hash()
			curr_user.token = token
			curr_user.password = encryption(new_password)
			curr_user.save()
			curr_access.last_otp_attempt = None
			curr_access.otp_attempts = 0
			curr_access.otp = None
			curr_access.otp_expiry_time = None
			curr_access.save()

			logs["data"]["status_message"] = "Password changed successfully for email ID {}.".format(email)
			logs["data"]["data_fields"] = [email]

			response["message"] = "Password changed successfully."
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
				curr_access.otp_attempts = 1
				curr_access.save()    
				logs["data"]["status_message"] = "Incorrect OTP for email ID {}.".format(email)
				logs["data"]["data_fields"] = [email]

				response["message"] = "Incorrect OTP."
				response["statuscode"] = 500

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
				response["statuscode"] = 500

				logs["added_at"] = datetime.utcnow()
				actvity_logs.insert_one(logs)
				return response
         
			elif timezone.now() > curr_access.last_otp_attempt + timedelta(minutes=time_threshold):
				"""
				If incorrect password request received after 'time_threshold' mins then refresh counters
				"""
				curr_access.last_otp_attempt = timezone.now()
				curr_access.otp_attempts = 1
				curr_access.save()    

				logs["data"]["status_message"] = "Incorrect OTP for email ID {}.".format(email)
				logs["data"]["data_fields"] = [email]

				response["message"] = "Incorrect OTP."
				response["statuscode"] = 500

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
