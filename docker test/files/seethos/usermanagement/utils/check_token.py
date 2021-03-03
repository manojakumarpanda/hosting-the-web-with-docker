from usermanagement.models import Users,AccessManagement
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
import logging
import datetime
import os, sys

from organization.models import UserCompanyRole

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_check_token(request_data, token):
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

		# Get all roles
		isAuthorized = True
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			isEverythingOk = False
			getUser = UserCompanyRole.objects.filter(user=curr_user, isActive=True, company__active=True, user__active=True)
			company_id = None
			role = None

			if len(getUser) > 0:
				allRoles = [usr.role.role_name for usr in getUser]
				logging.info(allRoles)
				if "SUPER-USER" in allRoles:
					getUser = UserCompanyRole.objects.filter(user=curr_user, role__role_name="SUPER-USER")[0]
					company_id = getUser.company.id
					role = "SUPER-USER"
				elif "COMPANY-ADMIN" in allRoles:
					getUser = UserCompanyRole.objects.filter(user=curr_user, role__role_name="COMPANY-ADMIN")[0]
					company_id = getUser.company.id
					role = "COMPANY-ADMIN"
				elif "PROJECT-ADMIN" in allRoles:
					getUser = UserCompanyRole.objects.filter(user=curr_user, role__role_name="PROJECT-ADMIN")[0]
					company_id = getUser.company.id
					role = "PROJECT-ADMIN"
				elif "USER" in allRoles:
					getUser = UserCompanyRole.objects.filter(user=curr_user, role__role_name="USER")[0]
					company_id = getUser.company.id
					role = "USER"

				if curr_user.expiry_date is None:
					isEverythingOk = True
				elif datetime.now() <= curr_user.expiry_date:
					isEverythingOk = True

			if isEverythingOk:
				logs["data"]["status_message"] = "Valid token."
				
				response["isUser"] = True
				response["role"] = role
				response["statuscode"] = 200
			else:
				logs["data"]["status_message"] = "Invalid token."
				
				response["isUser"] = False
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