from usermanagement.models import Users
from usermanagement.utils.hash import encryption, decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime
from uimanagement.models import CameraFeeds


def func_modifyCameraFeed(request_data, token):
    try:
        response = {}
        curr_user = Users.objects.filter(token=token)
        if len(curr_user) == 0:
            response["message"] = "Invalid Token."
            response["statuscode"] = 500
            return response
        else:
            try:
                cam_feed = CameraFeeds.objects.get(feedUid=request_data["feedUid"])
            except:
                response["message"] = "Invalid Feed ID"
                response["statuscode"] = 400
                return response
            try:
                cam_feed.feedName = request_data["feedName"]
                cam_feed.feedURL = request_data["feedURL"]
                cam_feed.camType = request_data["camType"]
                cam_feed.CamFeedObjects = str(request_data["objects"])
                cam_feed.save()
                response["statuscode"] = 200
                return response
            except:
                response["message"] = "Invalid Feed Details"
                response["statuscode"] = 400
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

