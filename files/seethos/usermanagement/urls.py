from django.urls import path
from . import views

urlpatterns = [
## Login	
    path('loginapi', views.login.as_view()),
    path('logout', views.logout.as_view())
]