from usermanagement.models import Users
from usermanagement.utils.hash import encryption, decryption
from uimanagement.models import CameraFeeds
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime


def func_addCameraFeed(request_data, token):
    try:
        response = {}
        curr_user = Users.objects.filter(token=token)
        if len(curr_user) == 0:
            response["message"] = "Invalid Token."
            response["statuscode"] = 500
            return response
        else:
            try:
                camFeed = CameraFeeds(
                    feedName=request_data["feedName"],
                    feedURL=request_data["feedURL"],
                    camType=request_data["camType"],
                    CamFeedObjects=str(request_data["objects"]),
                )
                camFeed.save()
                response["statuscode"] = 200
                return response
            except Exception as e:
                logging.info(e)
                response["message"] = "Feed Name or URL already exists"
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

