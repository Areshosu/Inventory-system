from Models.User import User
from Models.Permission import Permission
from Services.DbContext import DbContext

dbContext = DbContext(User)

from Services.UserManager import UserManager
from Services.PermissionManager import PermissionManager
userManager = UserManager()
permissionManager = PermissionManager()

#permissionManager.deleteAsync("e02feaee-2a37-4c96-b508-60a7644e9966")

userManager.createAsync({
    "username": "Alex123",
    "password": "password",
    "gender": "male",
    "age": 50,
    "permissionId": "e02feaee-2a37-4c96-b508-60a7644e9966"
})
