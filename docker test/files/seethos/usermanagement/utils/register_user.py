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

verify_link_exp = getattr(settings, "VERIFICATION_LINK_EXPIRY_DURATION", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def generate_hash():
	return uuid.uuid4().hex

def func_register_user(request_data, token):
	try:
		response={}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}

		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			logs["data"]["status_message"] = "Invalid Token."
			response['message'] = "Invalid Token."

			logs["added_at"] = datetime.datetime.utcnow()
			actvity_logs.insert_one(logs)
			response["statuscode"] = 400
			return response
		else:
			curr_user = curr_user[0]
			logs["User"] = curr_user.id

			# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user)

		# Get all roles
		isAuthorized = False
		for user in getUserCompanyRole:
			if user.role.role_name.upper() in ["SUPER-USER".upper(), "COMPANY-ADMIN".upper(), "PROJECT-ADMIN".upper()]:
				isAuthorized = True
				break
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL"]:
				apiParamsInfo[key] = value
		
		apiParamsInfo['password'] = encryption(random_alphaNumeric_string(5, 4))
		apiParamsInfo['token'] = generate_hash()
		apiParamsInfo['hashkey'] = generate_hash()[:10]
		if isAuthorized:
			apiParamsInfo["email"] = apiParamsInfo["email"].lower()
			getUser = Users.objects.filter(email=apiParamsInfo["email"])
			if len(getUser) == 0:
				getUser = Users.objects.create(**apiParamsInfo)
				verify_expiry = timezone.now() + datetime.timedelta(minutes=verify_link_exp)
				AccessManagement.objects.create(name=getUser, password_attempts=0, verification_link_expiry=verify_expiry)

				logs["data"]["data_fields"] = [apiParamsInfo["name"], apiParamsInfo["email"]]
				logs["data"]["status_message"] = "User created successfully."
				# Celery
				send_email.delay(str({"email": getUser.email,
										"subject": "New Registration",
										"template_name": "generate_passwords", 
										"variables": [decryption(apiParamsInfo['password'])],
										"email_type": "plain"
										}))

				response["data"] = getUser.id
				response['message'] = 'User created successfully.'
				response["statuscode"] = 200

			else:
				logs["data"]["data_fields"] = [apiParamsInfo["name"], apiParamsInfo["email"]]
				logs["data"]["status_message"] = 'User already existed.'
				response['message'] = 'User already existed.'
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [apiParamsInfo["name"], apiParamsInfo["email"]]
			logs["data"]["status_message"] = 'You are not authorized to create user.'
			response['message'] = 'You are not authorized to create user.'
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
		response["statuscode"] = 500
		return response