from usermanagement.models import Users,AccessManagement
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
import os,sys,logging
import datetime

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_logout(request_data):
	try:
		response = {}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}

		curr_user = Users.objects.filter(email=request_data["email"].lower())

		if len(curr_user) == 0:
			logs["data"]["status_message"] = "Invalid token."
			response['message'] = "Invalid token."
			response["statuscode"] = 400

			actvity_logs.insert_one(logs)
			return response
		else:
			curr_user = curr_user[0]
			logs["User"] = curr_user.id

		# curr_user.token = ""
		# curr_user.save()

		logs["data"]["status_message"] = "User logged out successfully."

		response['message'] = "User logged out successfully."
		response["statuscode"] = 200
		
		logs["added_at"] = datetime.datetime.utcnow()
		actvity_logs.insert_one(logs)
		return response			
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		logging.info("Login API error2-> "+str(e) + " " + str(exc_tb.tb_lineno))
		logs["data"]["status_message"] = "The username or password is not correct."
		actvity_logs.insert_one(logs)

		response['message']='The username or password is not correct'
		response["statuscode"]=400
		return response