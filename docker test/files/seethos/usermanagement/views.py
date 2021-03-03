from usermanagement.utils.login import func_login
from usermanagement.utils.reset_password_request import func_reset_password_request
from usermanagement.utils.register_user import func_register_user
from usermanagement.utils.signup_user import func_signup_user
from usermanagement.utils.create_role import func_create_role
from usermanagement.utils.get_role import func_get_role
from usermanagement.utils.delete_user import func_delete_user
from usermanagement.utils.edit_user import func_edit_user
from usermanagement.utils.edit_user_byid import func_edit_user_byid
from usermanagement.utils.update_password import func_update_password
from usermanagement.utils.set_new_password import func_set_new_password
from usermanagement.utils.check_token import func_check_token
from usermanagement.utils.logout import func_logout
from usermanagement.utils.list_user_byemail import func_list_user_byemail
from usermanagement.utils.download_file import func_download_file
from usermanagement.utils.validate_otp import func_validate_otp
from usermanagement.utils.send_otp import func_send_otp
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
import logging


class login(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		# request_data={'email':request.data['email'],'password':request.data['password']}
		# logging.info('Login_req=>>'+str(request_data))
		request_data = {**request_data, **newInfo}
		response = func_login(request_data)
		return Response(response)

class reset_password_request(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		response = func_reset_password_request(request_data)
		return Response(response)

class update_password(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		response = func_update_password(request_data)
		return Response(response)

class set_new_password(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_set_new_password(request_data, token)
		return Response(response)

class register_user(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_register_user(request_data, token)
		return Response(response)

class signup_user(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		# logging.info('View_api1==>{}'.format(request_data))
		response = func_signup_user(request_data)
		# logging.info('View_api==>{}'.format(response))
		return Response(response)

class logout(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		# token = request.META["HTTP_AUTHORIZATION"]
		response = func_logout(request_data)
		return Response(response)
		
class check_token(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_check_token(request_data,token)
		return Response(response)

class deactivate_user(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_delete_user(request_data, token)
		return Response(response)

class edit_user(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_user(request_data, token)
		return Response(response)

class edit_user_byid(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_user_byid(request_data, token)
		return Response(response)


class list_user_byemail(APIView):
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_user_byemail(request_data, token)
		return Response(response)

### Roles ##########
class create_role(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_role(request_data,token)
		return Response(response)

class get_role(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_get_role(request_data,token)
		return Response(response)		
## Download file get request
class download_file(APIView):
	def get(self, request):
		request_data = request.query_params
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]		
		response = func_download_file(request_data,token)
		return response	

#Manoj=
class validate_otp(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		# token = request.META["HTTP_AUTHORIZATION"]		
		response = func_validate_otp(request_data)
		return Response(response)

#Manoj=
class send_otp(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			"Requested_URL": request.META["REQUEST_URI"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		# token = request.META["HTTP_AUTHORIZATION"]		
		response = func_send_otp(request_data)
		return Response(response)	

