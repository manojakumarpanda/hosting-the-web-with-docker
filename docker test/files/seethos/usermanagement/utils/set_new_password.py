from usermanagement.models import Users, AccessManagement
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from organization.models import UserCompanyRole

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_set_new_password(request_data, token):
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
			response["statuscode"] = 400

			logs["added_at"] = datetime.datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response
		else:
			curr_user = curr_user[0]
			logs["User"] = curr_user.id

			# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user)

		# Get all roles
		isAuthorized = True
		# for user in getUserCompanyRole:
		# 	if user.role.role_name.upper() in "SUPER-USER".upper():
		# 		isAuthorized = True
		# 		break
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			# getUser = Users.objects.filter(id=apiParamsInfo["user"])
			getUser = curr_user

			# if len(getUser) > 0:
			# 	getUser = getUser[0]
			old_password = getUser.password
			
			if encryption(apiParamsInfo["old_password"]) == old_password:
			
				apiParamsInfo["updated_by"] = curr_user

				getUser.password = encryption(apiParamsInfo["new_password"])
				getUser.save()

				logs["data"]["data_fields"] = [getUser.email]
				logs["data"]["status_message"] = "Password changed successfully."

				response['message'] = 'Password changed successfully.'
				response["statuscode"] = 200
			
			else:
				logs["data"]["data_fields"] = [getUser.email]
				logs["data"]["status_message"] = "Old Password is Incorrect."
				response['message'] = "Old Password is Incorrect."
				response["statuscode"] = 400

			# else:
			# 	logs["data"]["data_fields"] = [apiParamsInfo["user"]]
			# 	logs["data"]["status_message"] = "User ID doesn't exist in database."
			# 	response['message'] = "User ID doesn't exist in database."
			# 	response["statuscode"] = 400

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