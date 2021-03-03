from django.urls import path
from . import views

urlpatterns = [
## Login	
    path('loginapi', views.login.as_view()),
    path('reset-password', views.reset_password_request.as_view()), #Forgot password #Works only with email integration
    path('update-password', views.update_password.as_view()), # THis API is used at forgot password stage
    path('new-password', views.set_new_password.as_view()),
    path('logout', views.logout.as_view()),
# ### Validate token	
    path('check-token', views.check_token.as_view()),	
# ### Email verification
#     path('validate-emailid', views.validate_emailid.as_view()), #GET REQUEST
# ## File upload / download	
#     path('upload-file', views.upload_file.as_view()),
    path('download-file', views.download_file.as_view()),
# ## Get activity logs	
    # path('list-activity-logs', views.list_activity_logs.as_view()),
## Roles
    path('create-role', views.create_role.as_view()),
    path('get-role', views.get_role.as_view()),
## User
    path('register-user', views.register_user.as_view()),
    path('signup', views.signup_user.as_view()),
    path('edit-user', views.edit_user.as_view()),
    path('edit-user-byid', views.edit_user_byid.as_view()),
    path('deactivate-user', views.deactivate_user.as_view()),
    path('list-user-byemail', views.list_user_byemail.as_view()),
    path('resend-otp', views.send_otp.as_view()),
    path('validate-otp', views.validate_otp.as_view()),
]