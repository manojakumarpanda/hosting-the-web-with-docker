from usermanagement.models import Users, AccessManagement, Roles
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


def func_list_user_byemail(request_data, token):
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

			actvity_logs.insert_one(logs)
			return response
		else:
			curr_user = curr_user[0]
			logs["User"] = curr_user.id

			# # Get UserCompanyRole
			# getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user, 
			# 													user__active=True,
			# 													company__id=request_data["company_id"],
			# 													company__active=True, 
			# 													role__active=True, 
			# 													isActive=True)

		# Get all roles
		isAuthorized = True
		# displayData = None
		# for user in getUserCompanyRole:
		# 	if user.role.role_name.upper() in ["SUPER-USER"]:
		# 		isAuthorized = True
		# 		displayData = 'ALL'
		# 		break
		# 	elif user.role.role_name.upper() in ["COMPANY-ADMIN"]:
		# 		isAuthorized = True
		# 		displayData = 'COMPANY-LEVEL'
		# 		break
		# 	elif user.role.role_name.upper() in ["PROJECT-ADMIN"]:
		# 		isAuthorized = True
		# 		displayData = 'PROJECT-LEVEL'
		# 		break

		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			data = None
			apiParamsInfo["email"] = apiParamsInfo["email"].lower()
			getUser = Users.objects.filter(email__iexact=apiParamsInfo["email"])
			if len(getUser) > 0:
				user = getUser[0]
				response["data"] = {
					"id": user.id,
					"first_name": user.first_name,
					"last_name": user.last_name,
					"name": user.name,
					"email": user.email,
					"status": user.active,
					"phone_no": user.phone_no,
					"created_on": user.created_at,
					"designation": user.designation,
					"reporting_manager_id": user.reporting_manager_id,
					"reporting_manager_name": user.reporting_manager_name,
					"reporting_manager_email": user.reporting_manager_email,
				}
				logs["data"]["status_message"] = "Users listed successfully."
				response['message'] = "Users listed successfully."
				response["statuscode"] = 200

			else:
				logs["data"]["status_message"] = "No user found corresponding to the email."
				response['message'] = "No user found corresponding to the email."
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