from __future__ import absolute_import
from celery import shared_task
from usermanagement.utils.send_email import SendEmail
from celery.task import periodic_task
from celery.task.schedules import crontab
import datetime
import time

from project.models import *
from project.models import *

#manoj-Testing

#this is to execute and sending the message on hourly for those who select hourly as frequency  
@periodic_task(run_every=crontab(minute=1),ignore_result=False)
def send_minute():
	try:
		email='abc@email.com'
		message='celery beat messages'
		time.sleep(10)
		print('Email is sent to {} and the body of the eamil is:-{}'.format(email,message))
		
	except Exception as e:
		print('Exceptions==>'+str(e))

#this is to execute and sending the message on hourly for those who select hourly as frequency  
@periodic_task(run_every=crontab(hour=1,minute=0),ignore_result=False)
def send_hourly():
	try:
		email='abc@email.com'
		message='celery beat messages'
		time.sleep(10)
		print('Email is sent to {} and the body of the eamil is:-{}'.format(email,message))
		
	except Exception as e:
		print('Exceptions==>'+str(e))

#this is to execute and sending the message on daily for those who select daily as frequency  
@periodic_task(run_every=crontab(minute=0, hour=0),ignore_result=False)
def send_daily():
	try:
		email='abcd@email.com'
		message='celery beat daily messages'
		time.sleep(10)
		print('Email is sent to {} and the body of the eamil is:-{}'.format(email,message))
		
	except Exception as e:
		print('Exceptions==>'+str(e))

#this is to execute and sending the message on weekly for those who select weekly as frequency  
@periodic_task(run_every=crontab(minute=0, hour=0,day_of_week='sunday'),ignore_result=False)
def send_weekly():
	try:
		email='abcd@email.com'
		message='celery beat weekly messages'
		time.sleep(10)
		print('Email is sent to {} and the body of the eamil is:-{}'.format(email,message))
		
	except Exception as e:
		print('Exceptions==>'+str(e))
  
#this is to execute and sending the message on monthly for those who select monthly as frequency  
@periodic_task(run_every=crontab(0, 0, day_of_month='1'),ignore_result=False)
def send_month():
	try:
		email='abcd@email.com'
		message='celery beat monthly on the 1st date of month messages'
		time.sleep(10)
		print('Email is sent to {} and the body of the eamil is:-{}'.format(email,message))
		
	except Exception as e:
		print('Exceptions==>'+str(e))
  
  