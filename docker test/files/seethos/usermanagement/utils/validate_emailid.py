from rest_framework.response import Response
from usermanagement.models import Users,AccessManagement
import logging
import uuid
from usermanagement.utils.hash import encryption,decryption
from usermanagement.utils.send_email import SendEmail
from django.utils import timezone
from django.conf import settings
import datetime
from datetime import timedelta
media_files_path = getattr(settings, "MEDIA_ROOT", None)
server_url = getattr(settings, "SERVERURL", None)
verify_link_exp = getattr(settings, "VERIFICATION_LINK_EXPIRY_DURATION", None)


def generate_hash():
	return uuid.uuid4().hex

def func_validate_emailid(request_data):	
	try:
		token2=generate_hash()
		response={}
		# request_data=request.data
		# logging.info(str(request_data))
		# request_data = request.query_params		
		token=str(request_data["uid"])
		curr_user = Users.objects.filter(token=token)[0]
		curr_access = AccessManagement.objects.filter(name=curr_user)[0]
		if curr_user.user_verified is True:
			# return HttpResponseRedirect(redirect_to= server_url + '/login/')
			return 0
		else:    
			if timezone.now() > curr_access.verification_link_expiry:
				curr_user.token=token2
				curr_user.save()
				verify_expiry = timezone.now()+timedelta(minutes=verify_link_exp)
				curr_access.verification_link_expiry=verify_expiry
				curr_access.save()
				body="Email :"+ curr_user.email +'\n'+ '\n'+'Click on this link to verify - '+ server_url + "/access/validate-emailid?uid=" + str(token2)
				# subject = "FSMA - Account verification"
				# SendEmail(curr_user.email,body,subject)
				# return render(request,'verifysignup.html',context={'x':1})
				return 1 #Link expired
			else:
				curr_user.user_verified=True
				curr_user.token=token2
				curr_user.save()
				curr_access.verification_link_expiry = None	
				# return render(request,'verifysignup.html',context={'x':2})		
				return 2 #User activated
	except Exception as e:
		logging.info("verify user error-> "+str(e))
		# return HttpResponseRedirect(redirect_to= server_url + '/login/')
		return 0


