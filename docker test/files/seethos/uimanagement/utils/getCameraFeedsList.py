import ast
import datetime
import logging
import os
import re
import sys

from django.conf import settings
from uimanagement.models import CameraFeeds
from usermanagement.models import Users
from usermanagement.utils.hash import decryption, encryption


def func_getCameraFeedsList(request_data, token):
    try:
        response = {}
        curr_user = Users.objects.filter(token=token)
        if len(curr_user) == 0:
            response["message"] = "Invalid Token."
            response["statuscode"] = 500
            return response
        else:
            FeedsObj = CameraFeeds.objects.all()
            ret_arr = []
            for obj in FeedsObj:
                temp_obj = {}
                temp_obj["feedUid"] = obj.feedUid
                temp_obj["feedName"] = obj.feedName
                temp_obj["feedURL"] = obj.feedURL
                temp_obj["camType"] = obj.camType
                try:
                    if type(ast.literal_eval(obj.CamFeedObjects)) is list:
                        temp_obj["objects"] = ast.literal_eval(obj.CamFeedObjects)
                    else:
                        temp_obj["objects"] = ""
                except:
                    temp_obj["objects"] = ""
                ret_arr.append(temp_obj)
            response["data"] = ret_arr
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
