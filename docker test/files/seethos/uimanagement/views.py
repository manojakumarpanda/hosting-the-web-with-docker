import logging

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.addCameraFeed import func_addCameraFeed
from .utils.createEvents import func_addEvent
from .utils.getCameraFeedsList import func_getCameraFeedsList
from .utils.modifyCameraFeed import func_modifyCameraFeed
from .utils.processManagement import (
    func_startObjectDetectionProcess,
    func_stopObjectDetectionProcess,
    func_getProcessStatus,
)
from .utils.saveCameraTypeSettings import func_saveCameraTypeSettings
from .utils.getCameraTypeSettings import func_getCameraTypeSettings
from .utils.deleteCameraFeed import func_deleteCameraFeed
from .utils.uploadAlarmFile import func_uploadAlarmFile
from .utils.deleteAlarm import func_deleteAlarm
from .utils.listAlarms import func_listAlarms


#  from .utils.startObjectDetectionProcess import func_startObjectDetectionProcess
#  from .utils.stopObjectDetectionProcess import func_stopObjectDetectionProcess


class getCameraFeedsList(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_getCameraFeedsList(request_data, token)
        return Response(response)


class startObjectDetectionProcess(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_startObjectDetectionProcess(request_data, token)
        return Response(response)


class stopObjectDetectionProcess(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_stopObjectDetectionProcess(request_data, token)
        return Response(response)


class addCameraFeed(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_addCameraFeed(request_data, token)
        return Response(response)


class modifyCameraFeed(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_modifyCameraFeed(request_data, token)
        return Response(response)


class saveCameraTypeSettings(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_saveCameraTypeSettings(request_data, token)
        return Response(response)


class addEvent(APIView):
    def post(self, request):
        request_data = request.data
        response = func_addEvent(request_data)
        return Response(response)


class searchEvents(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_searchEvents(request_data, token)
        return Response(response)
		
		
class getCameraTypeSettings(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_getCameraTypeSettings(request_data, token)
        return Response(response)

class deleteCameraFeed(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_deleteCameraFeed(request_data, token)
        return Response(response)

class getProcessStatus(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_getProcessStatus(request_data, token)
        return Response(response)
		
		
class uploadAlarmFile(APIView):
    def post(self, request):
        request_data = request.data
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_uploadAlarmFile(request_data, token)
        return Response(response)		
		
class deleteAlarm(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_deleteAlarm(request_data, token)
        return Response(response)

class listAlarms(APIView):
    def post(self, request):
        request_data = request.data
        request_data = {**request_data}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_listAlarms(request_data, token)
        return Response(response)
		
