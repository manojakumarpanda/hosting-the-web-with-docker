import logging
import os
import sys
import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from usermanagement.models import Users
from usermanagement.utils.hash import decryption, encryption

default_email = "admin@seethos.com"
default_password = "newPassword@123"


def add_admin():
	try:
		pasw = encryption(default_password)
		logging.info(pasw)
		token = uuid.uuid4().hex
		Users.objects.create(firstName="Seethos",lastName="Admin",email=default_email,mobile="123123123123",password=pasw,token=token)
		logging.info("User created")
	except Exception as e:
		logging.info("Error in creating user error")
		logging.info(str(e))


def generate_hash():
	return uuid.uuid4().hex

def func_login(request_data):
	try:
		response = {}
		# request_data = request.data
		email =request_data["email"]
		email=email.lower()
		password=request_data["password"]
		curr_user = Users.objects.filter(email=email)		
		if email == default_email and len(curr_user) == 0:
			add_admin()
		curr_user = Users.objects.filter(email=email)				
		if len(curr_user) == 0:
			response['message'] = "Invalid User"
			response["statuscode"] = 400
			return response
		else:
			curr_user = curr_user[0]
		if curr_user.password == encryption(str(password)):			
			response["statuscode"] = 200
			token = uuid.uuid4().hex
			curr_user.token = token
			curr_user.save()
			response["token"] = token
			return response	
		else:
			response['message'] = "Invalid Password"
			response["statuscode"] = 400
			return response			
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		logging.error("Login API error-> "+str(e) + " " + str(exc_tb.tb_lineno))
		response['message']='The username or password is not correct'
		response["statuscode"]=400
		return response
