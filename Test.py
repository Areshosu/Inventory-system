from Models.User import User
from Models.Permission import Permission
from Services.DbContext import DbContext

dbContext = DbContext(Permission)

from Services.UserManager import UserManager
from Services.PermissionManager import PermissionManager
userManager = UserManager()
permissionManager = PermissionManager()

permissionManager.deleteAsync("4dcdd026-c5e3-4961-8459-f03d4b417399")

# userManager.createAsync({
#     "username": "Alex123",
#     "password": "password",
#     "gender": "male",
#     "age": 50,
#     "permissionId": "e02feaee-2a37-4c96-b508-60a7644e9966"
# })
