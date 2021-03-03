from usermanagement.models import Users,AccessManagement
from usermanagement.utils.hash import encryption,decryption
# from usermanagement.utils.store_activity_logs import func_store_activity_logs
from django.conf import settings
from django.utils import timezone
refresh_lockout = getattr(settings, "LOCKOUT_COUNT_RESET_DURATION", None)
time_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS", None)
superuser = getattr(settings, "SUPERUSER", None)
superuser_pass = getattr(settings, "SUPERUSERPASS", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)
import logging,uuid,os,sys
from datetime import timedelta, datetime

from organization.models import UserCompanyRole

def generate_hash():
	return uuid.uuid4().hex

def func_login(request_data):
	logs={"data": {
			}}
	try:
		# logging.info('Request=>'+str(request_data))
		response = {}
		email =request_data["email"]
		# email=email.lower()
		password=request_data["password"]

		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}

		curr_user = Users.objects.filter(email__iexact=email)

		if len(curr_user) == 0:
			logs["data"]["status_message"] = "Invalid email."
			response['message'] = "Invalid Email."
			response["statuscode"] = 400

			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)
			return response
		else:
			curr_user = curr_user[0]
			logs["User"] = curr_user.id

		curr_access = AccessManagement.objects.filter(name = curr_user)[0]
		# logging.info("Login-> "+ curr_user.token)
		"""
		Check if account isnt locked for access
		1. If password attempts count is equal 'count_threshold' and user tried to login again within 'time_threshold' mins of last attempt then freeze the account
		2. Password attempts count is reset everytime user correctly logs in
		3. Password attempts count is incremented every time an wrong passwor is entered within 'time_threshold' minutes of last password attempt
		"""
		if curr_access.last_login_attempt is not None:
			if timezone.now() < curr_access.last_login_attempt + timedelta(minutes=refresh_lockout) and curr_access.password_attempts == count_threshold:
				logs["data"]["status_message"] = "Multiple invalid password attempts."

				logs["added_at"] = datetime.utcnow()
				actvity_logs.insert_one(logs)

				response["message"] = "Multiple invalid password attempts. Please try after sometime"
				response["statuscode"] = 400
				return response
			elif timezone.now() >= curr_access.last_login_attempt + timedelta(minutes=refresh_lockout) and curr_access.password_attempts == count_threshold:
				"""
				Rest counters after lockout period is expired. FLow does not break here
				"""
				curr_access.last_login_attempt = None
				curr_access.password_attempts = 0
				curr_access.save()
			else:
				pass
		try:
			"""
			last_login_attempt is set to None when correct password request is received
			"""
			
			if curr_user.password == encryption(str(password)):
				if curr_user.user_verified is None or curr_user.user_verified ==0:
					logs["data"]["status_message"] = "Account is Inactive."

					logs["added_at"] = datetime.utcnow()
					actvity_logs.insert_one(logs)

					response["statuscode"]=400
					response["message"] = "Your account is not active. Please click on the link sent to your email at the time of Registration."
					return response
				else:
					# token = generate_hash()
					# curr_user.token = token
					curr_access.last_login_attempt = None
					curr_user.save()
					curr_access.password_attempts = 0
					curr_access.save()
					# func_store_activity_logs(curr_user,"Login","")

					isEverythingOk = False

					getUser = UserCompanyRole.objects.filter(user=curr_user)
					company_id = None
					role = None

					if len(getUser) > 0:
						allRoles = [usr.role.role_name for usr in getUser]
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
						logs["data"]["status_message"] = "Successful login into account."

						logs["added_at"] = datetime.utcnow()
						actvity_logs.insert_one(logs)

						response["statuscode"] = 200
						response["token"] = curr_user.token
						response["name"] = curr_user.name
						response["email"] = curr_user.email
						response["company_id"] = company_id
						response["role"] = role
						# logging.info("Login-> "+ str(response))
						# logging.info("Login-> "+ str(curr_user.token))
						return response
					else:
						logs["data"]["status_message"] = "Unsuccessful login into account."

						logs["added_at"] = datetime.utcnow()
						actvity_logs.insert_one(logs)

						response["statuscode"] = 400
						return response
			else:
				"""
				last_login_attempt is set only when the first wrong password request is received
				"""
				if curr_access.last_login_attempt is None:
					curr_access.last_login_attempt = timezone.now()
					curr_access.password_attempts = 1
					curr_access.save()
					logs["data"]["status_message"] = "Password is incorrect."

					logs["added_at"] = datetime.utcnow()
					actvity_logs.insert_one(logs)
					logging.info('Password is in correct')
					response['message']='The username or password is not correct'
					response["statuscode"]=400
					return response                            
				elif timezone.now() < curr_access.last_login_attempt + timedelta(minutes=time_threshold):
					if curr_access.password_attempts == count_threshold - 1: #This will help add a lockout delta to last login attempt
						curr_access.last_login_attempt = timezone.now()
					curr_access.password_attempts = curr_access.password_attempts + 1
					curr_access.save()
					logs["data"]["status_message"] = "Password is incorrect."

					logs["added_at"] = datetime.utcnow()
					actvity_logs.insert_one(logs)
					logging.info('Password incorrect 2')
					response['message']='The username or password is not correct'
					response["statuscode"]=400
					return response                            
				elif timezone.now() > curr_access.last_login_attempt + timedelta(minutes=time_threshold):
					"""
					If incorrect password request received after 'time_threshold' mins then refresh counters
					"""
					curr_access.last_login_attempt = timezone.now()
					curr_access.password_attempts = 1
					curr_access.save()
					logs["data"]["status_message"] = "Password is incorrect."

					logs["added_at"] = datetime.utcnow()
					actvity_logs.insert_one(logs)
					logging.info('Password incorrect3')
					response['message']='The username or password is not correct'
					response["statuscode"]=400
					return response  
		except Exception as e:
			logs["data"]["status_message"] = "The username or password is not correct."

			logs["added_at"] = datetime.utcnow()
			actvity_logs.insert_one(logs)

			exc_type, exc_obj, exc_tb = sys.exc_info()
			logging.info("Login API error2-> "+str(e) + " " + str(exc_tb.tb_lineno))
			response['message']='The username or password is not correct'
			response["statuscode"]=400
			return response
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		logging.info("Login API error2-> "+str(e) + " " + str(exc_tb.tb_lineno))
		logs["data"]["status_message"] = "The username or password is not correct."
		actvity_logs.insert_one(logs)

		response['message']='The username or password is not correct'
		response["statuscode"]=400
		return response
