from django.urls import path
from . import views

urlpatterns = [
    path("startObjectDetectionProcess", views.startObjectDetectionProcess.as_view()),
    path("stopObjectDetectionProcess", views.stopObjectDetectionProcess.as_view()),
    path("getCameraFeedsList", views.getCameraFeedsList.as_view()),
    path("addCameraFeed", views.addCameraFeed.as_view()),
    path("modifyCameraFeed", views.modifyCameraFeed.as_view()),
    path("deleteCameraFeed", views.deleteCameraFeed.as_view()),	
    path("saveCameraTypeSettings", views.saveCameraTypeSettings.as_view()),
    path("getCameraTypeSettings", views.getCameraTypeSettings.as_view()),
    path("searchEvents", views.searchEvents.as_view()),
    path("getProcessStatus", views.getProcessStatus.as_view()),
    path("uploadAlarmFile", views.uploadAlarmFile.as_view()),
    path("deleteAlarm", views.deleteAlarm.as_view()),
    path("listAlarms", views.listAlarms.as_view()),
]
