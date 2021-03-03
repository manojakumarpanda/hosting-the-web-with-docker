from django.db import models
from django.utils import timezone

# Create your models here.
class Users(models.Model):
	userUid = models.AutoField(primary_key=True,db_column='userUid')
	firstName = models.CharField(max_length=255,blank=False,null=False,db_column='firstName')
	lastName = models.CharField(max_length=255,blank=False,null=False,db_column='lastName')
	password = models.CharField(max_length=2000,blank=False,null=False,db_column='password')
	token = models.CharField(max_length=2000,db_column='token')
	email = models.CharField(max_length=255,unique=True,blank=False,null=False,db_column='email')
	mobile = models.CharField(max_length=255,blank=False,null=False,db_column='mobile')
	createdDate = models.DateTimeField(auto_now_add=timezone.now(),db_column='createdDate')
	modifiedDate = models.DateTimeField(auto_now=True,db_column='modifiedDate')
	class Meta:
		db_table = 'Users'