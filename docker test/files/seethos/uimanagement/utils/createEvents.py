import logging
import os
import sys

from django.conf import settings
from django.db import IntegrityError

from ..models import Events


def func_addEvent(request_data):
    try:
        response = {}
        try:
            event = Events(
                camFeedId=request_data["camera_id"],
                eventTime=request_data["etime"],
                objsDetected=request_data["objects"],
                videoPath=request_data["video_path"],
            )
            event.save()
            response["statuscode"] = 200
        except Exception as e:
            logging.error(e)
            response["message"] = "Unable to save event"
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
