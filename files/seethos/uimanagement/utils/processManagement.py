import ast
import datetime
import logging
import os
import re
import sys
from enum import Enum

# from detector.main import create_video_process, stop_processes
from django.conf import settings
from django.db import IntegrityError

from usermanagement.models import Users

from ..models import CameraFeeds, CameraSettings,ProcessState

logger = logging.getLogger(__name__)


class ProcessState(Enum):
	RUNNING = 1
	STOPPED = 0


process_state = ProcessState.STOPPED


def func_startObjectDetectionProcess(request_data, token):
	global process_state
	try:
		response = {}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response["message"] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			cameras = CameraFeeds.objects.all()

			if process_state == ProcessState.STOPPED:
				for camera in cameras:
					rectColours = CameraSettings.objects.filter(camType=camera.camType)[
						0
					].rectColours

					create_video_process(
						camera.feedUid,
						camera.feedName,
						camera.feedURL,
						ast.literal_eval(rectColours),
					)
				process_state = ProcessState.RUNNING

			response["statuscode"] = 200
			return response
	except Exception as e:
		process_state = ProcessState.STOPPED
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logger.error(
			str(exc_type)
			+ " "
			+ str(fname)
			+ " "
			+ str(exc_tb.tb_lineno)
			+ " "
			+ str(e)
		)
		response["message"] = "There was some error"
		response["statuscode"] = 400
		return response


def func_stopObjectDetectionProcess(request_data, token):
	global process_state
	try:
		response = {}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response["message"] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			response["status"] = process_state
			response["statuscode"] = 200
			return response
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.info(
			str(exc_type)
			+ " "
			+ str(fname)
			+ " "
			+ str(exc_tb.tb_lineno)
			+ " "
			+ str(e)
		)
		response["message"] = "There was some error"
		response["statuscode"] = 400
		return response
		
		
def func_getProcessStatus(request_data, token):
	global process_state
	try:
		response = {}
		curr_user = Users.objects.filter(token=token)
		if len(curr_user) == 0:
			response["message"] = "Invalid Token."
			response["statuscode"] = 500
			return response
		else:
			response["status"] = process_state
			response["statuscode"] = 200
			return response
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.info(
			str(exc_type)
			+ " "
			+ str(fname)
			+ " "
			+ str(exc_tb.tb_lineno)
			+ " "
			+ str(e)
		)
		response["message"] = "There was some error"
		response["statuscode"] = 400
		return response