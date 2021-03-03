from usermanagement.models import Users,AccessManagement
from usermanagement.tasks import send_email
import random
import string
import uuid
import logging
import os,sys
from django.utils import timezone
import datetime
from usermanagement.utils.hash import encryption, decryption, random_alphaNumeric_string
from django.conf import settings

media_files_path = getattr(settings, "MEDIA_ROOT", None)
server_url = getattr(settings, "SERVERURL", None)
otp_expiry_duration = getattr(settings, "OTP_EXPIRY_DURATION", None)
refresh_lockout = getattr(settings, "LOCKOUT_PASSWORD_RESET_INIT_DURATION", None)
time_threshold = getattr(settings, "PASSWORD_RESET_INIT_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "PASSWORD_RESET_INIT_COUNT_MAX_ATTEMPTS", None)
front_end_url = getattr(settings, "FRONT_END_URL", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_send_otp(request_data):
	try:
		response = {}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}

		# Check if EMAIL exists in database
		curr_user = Users.objects.filter(id=request_data["user_id"])
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
				logs["added_at"] = datetime.datetime.utcnow()
				actvity_logs.insert_one(logs)
				return response
		else:
			logs["data"]["status_message"] = "User with this id {} does not exists in the database.".format(request_data["user_id"])
			logs["data"]["data_fields"] = [email]
			response["message"] = "User with this id {} does not exists in the database.".format(request_data["user_id"])
			response["statuscode"] = 400
			logs["added_at"] = datetime.datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response

		np =''.join(random.choice(string.digits) for i in range(6))
		curr_access.otp = encryption(np)
		curr_access.otp_attempts = 0
		curr_access.last_otp_attempt = None
		curr_access.otp_expiry_time = timezone.now() + datetime.timedelta(minutes=otp_expiry_duration)
  
		if curr_access.last_otp_attempt is None:
			curr_access.last_otp_attempt = timezone.now()
			curr_access.save()
		elif timezone.now() < curr_access.otp_expiry_time:
			curr_access.otp_expiry_time = timezone.now() + datetime.timedelta(minutes=otp_expiry_duration)
			curr_access.save()
		elif timezone.now()>curr_access.otp_expiry_time:
			curr_access.otp_expiry_time = timezone.now() + datetime.timedelta(minutes=otp_expiry_duration)
			curr_access.last_otp_attempt = timezone.now()
			curr_access.otp = encryption(np)
			curr_access.otp_attempts = 0
			curr_access.save()

		subject= "CRM OTP For Company Creation- " + datetime.date.today().strftime("%d-%m-%Y")

		# Celery
		send_email.delay(str({"email": curr_user.email,
								"subject": subject,
								"template_name": "otp_mail", 
								"variables": [curr_user.email, np, curr_user.email],
								"email_type": "plain"
								}))

		logs["data"]["status_message"] = "OTP to email ID {} sent successfully.".format(email)
		logs["data"]["data_fields"] = [email]
		response["message"] = "OTP to email ID {} sent successfully.".format(email)
		response["statuscode"] = 200
		logs["added_at"] = datetime.datetime.utcnow()
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


