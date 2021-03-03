from django.db import models
from django.utils import timezone

class Alarms(models.Model):
	alarmUid = models.AutoField(primary_key=True, db_column="alarmUid")
	alarmName = models.CharField(max_length=255, unique=True, blank=False, null=False,db_column="alarmName")
	originalFileName = models.TextField(blank=False, null=False, db_column="originalFileName")
	datafile = models.FileField(blank=False,null=False)	
	createdDate = models.DateTimeField(auto_now_add=timezone.now(), db_column="createdDate")
	modifiedDate = models.DateTimeField(auto_now=True, db_column="modifiedDate")
	class Meta:
		db_table = "Alarms"	
		
		
class CameraFeeds(models.Model):
	feedUid = models.AutoField(primary_key=True, db_column="feedUid")
	feedName = models.CharField(
		max_length=255, unique=True, blank=False, null=False, db_column="feedName"
	)
	camType = models.CharField(
		max_length=255, blank=False, null=False, db_column="camType"
	)
	feedURL = models.CharField(
		max_length=2000, unique=True, blank=False, null=False, db_column="feedURL"
	)
	CamFeedObjects = models.TextField(blank=False, null=False, db_column="objects")
	createdDate = models.DateTimeField(
		auto_now_add=timezone.now(), db_column="createdDate"
	)
	modifiedDate = models.DateTimeField(auto_now=True, db_column="modifiedDate")

	class Meta:
		db_table = "CameraFeeds"


class CameraSettings(models.Model):
	id = models.AutoField(primary_key=True, db_column="id")
	camType = models.CharField(
		max_length=255, unique=True, blank=False, null=False, db_column="camType"
	)
	alarm= models.ForeignKey(Alarms,blank=True, null=True,on_delete=models.PROTECT)
	rectColours = models.TextField(blank=False, null=False, db_column="rectColours")
	createdDate = models.DateTimeField(
		auto_now_add=timezone.now(), db_column="createdDate"
	)
	modifiedDate = models.DateTimeField(auto_now=True, db_column="modifiedDate")

	class Meta:
		db_table = "CameraSettings"


class Events(models.Model):
	eventUid = models.AutoField(primary_key=True, db_column="eventUid")
	camFeedId = models.IntegerField(blank=False, null=False, db_column="camFeedId")
	eventTime = models.DateTimeField(blank=False, null=False, db_column="eventTime")
	objsDetected = models.TextField(blank=False, null=False, db_column="objsDetected")
	videoPath = models.CharField(
		max_length=2000, unique=True, blank=False, null=False, db_column="videoPath"
	)
	createdDate = models.DateTimeField(
		auto_now_add=timezone.now(), db_column="createdDate"
	)
	modifiedDate = models.DateTimeField(auto_now=True, db_column="modifiedDate")

	class Meta:
		db_table = "Events"
		
class ProcessState(models.Model):
	status = models.IntegerField(default=0, db_column="status")
	class Meta:
		db_table = "ProcessState"
