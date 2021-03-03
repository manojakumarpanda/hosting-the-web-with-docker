from usermanagement.utils.login import func_login
from usermanagement.utils.logout import func_logout

from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
import logging


class login(APIView):
	def post(self, request):
		request_data = request.data
		request_data = {**request_data}
		response = func_login(request_data)
		return Response(response)

class logout(APIView):
	def post(self, request):
		request_data=request.data
		request_data = {**request_data}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_logout(request_data, token)
		return Response(response)
