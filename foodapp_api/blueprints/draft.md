What API do we need?


API 1: Chef
endpoint: /chef

1. GET /chef/all 		
to return list of chefs



POST /chef		[to sign up as chef, with all details]
POST /chef/login	[to login as chef]
GET /chef/<id>		[to return chef profile]
GET /chef/<id>/booking	[to return chef booking -current/past]
GET /chef/check_name 	[check if a username for chef is available]

API 2: User
endpoint: /user

POST /user		[to sign up as user]
POST /user/login	[to login as user]
GET /user/<id>		[return user profile]
GET /user/
GET /user/check_name 	[check if a username for user is available]







