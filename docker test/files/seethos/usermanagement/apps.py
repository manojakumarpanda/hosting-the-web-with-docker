from django.apps import AppConfig


class UsermanagementConfig(AppConfig):
	name = 'usermanagement'

	def ready(self):
		try:
			from .models import Users, Roles, AccessManagement
			from .utils.hash import encryption
			import uuid

			users = [{
				"first_name": "CRM",
				"last_name": "Super User 1",
				"name": "CRM Super User 1",
				"email": "superuser@momenttext.com",
				"password": encryption("Password@123"),
				"token": uuid.uuid4().hex,
				"designation": "SuperUser",
				"active": True,
				"user_verified": True,
				"reporting_manager_id": "67890",
				"reporting_manager_name": "Rohit Khandelwal",
				"reporting_manager_email": "shivain.mattoo1@kpmg.com",
				"hashkey": uuid.uuid1().hex
			}]

			for user in users:
				isAlreadyAvailable = Users.objects.filter(email=user["email"])
				if len(isAlreadyAvailable) == 0:
					user = Users.objects.create(**user)
					AccessManagement.objects.create(name=user)
				else:
					isAccesManageAvailable = AccessManagement.objects.filter(name=isAlreadyAvailable[0])
					if len(isAccesManageAvailable) == 0:
						AccessManagement.objects.create(name=isAlreadyAvailable[0])


			roles = [
				{
					"role_name": "SUPER-USER",
					"created_by": 1,
					"updated_by": 1,
				},
				{
					"role_name": "COMPANY-ADMIN",
					"created_by": 1,
					"updated_by": 1,
				},
				{
					"role_name": "PROJECT-ADMIN",
					"created_by": 1,
					"updated_by": 1,
				},
				{
					"role_name": "USER",
					"created_by": 1,
					"updated_by": 1,
				}
			]

			for role in roles:
				getRole = Roles.objects.filter(role_name=role["role_name"].upper())

				if len(getRole) == 0:
					role["created_by"] = Users.objects.filter(id=role["created_by"])[0]
					role["updated_by"] = Users.objects.filter(id=role["updated_by"])[0]

					getRole = Roles.objects.create(**role)
		except:
			pass
				