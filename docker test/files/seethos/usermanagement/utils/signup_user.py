from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption, random_alphaNumeric_string
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
from django.utils import timezone
import datetime
import uuid

from usermanagement.models import Users, AccessManagement
from usermanagement.tasks import send_email

from organization.models import UserCompanyRole
from usermanagement.utils.send_otp import func_send_otp

verify_link_exp = getattr(settings, "VERIFICATION_LINK_EXPIRY_DURATION", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)
otp_expiry_duration=getattr(settings,'OTP_EXPIRY_DURATION')



def generate_hash():
	return uuid.uuid4().hex

def func_signup_user(request_data):
	try:
		response={}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}
		
		apiParamsInfo = {}
		
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL"]:
				apiParamsInfo[key] = value
		password=encryption(random_alphaNumeric_string(5, 4))
		
		apiParamsInfo['password'] =encryption(password)
		apiParamsInfo['token'] = generate_hash()
		apiParamsInfo['email'] = request_data['email'].lower()
		apiParamsInfo['hashkey'] = generate_hash()[:10]
		apiParamsInfo['name']=' '.join((request_data['first_name'],request_data['last_name']))
		apiParamsInfo['first_name']=request_data['first_name']
		apiParamsInfo['last_name']=request_data['last_name']
		getUser=Users.objects.filter(email__iexact=request_data['email'])
		if len(getUser) == 0:
			getUser = Users.objects.create(**apiParamsInfo)
			# Celery
			send_email.delay(str({"email": getUser.email,
										"subject": "New Registration",
										"template_name": "generate_passwords", 
										"variables": [apiParamsInfo["name"],decryption(apiParamsInfo['password'])],
										"email_type": "html"
										}))
			if getUser:
				verify_expiry = timezone.now() + datetime.timedelta(minutes=verify_link_exp)
				AccessManagement.objects.create(name=getUser, password_attempts=0, verification_link_expiry=None)		
				resp_data=func_send_otp(request_data)
				logging.info('Response of Otp send==>'+str(resp_data))
			response["id"] = getUser.id
			response["timer"] = otp_expiry_duration
			response['message'] = 'User registered successfully.'
			response["statuscode"] = 200
			logs["added_at"] = datetime.datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response
		else:
			logs["data"]["data_fields"] = [apiParamsInfo["first_name"], apiParamsInfo["email"]]
			logs["data"]["status_message"] = 'User already registered.'
			response['message'] = 'User already registered.'
			response["statuscode"] = 400
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
		response["message"] = 'Fill all data to register user'
		response["statuscode"] = 500
		return response