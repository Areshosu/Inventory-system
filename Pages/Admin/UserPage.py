import json
from typing import Type
from Services.Console import *
from Services.UserManager import UserManager
from Services.PermissionManager import PermissionManager

class UserPage:
    def __init__(self, userManager: Type[UserManager], permissionManager: Type[PermissionManager]):
        self.userManager = userManager
        self.permissionManager = permissionManager
        self.menuPage()

    def menuPage(self):
        clear_console()
        option = int(input("How would you like to manage Users? \n\n" \
                                "[0] Show User List \n" \
                                "[1] Find User \n" \
                                "[2] Create User \n" \
                                "[3] Update User \n" \
                                "[4] Delete User \n" \
                                "[5] Return to Main Menu \n\n" \
                                "Select Item [0-5] (Default 0): ") or 0)
        
        clear_console()
        if (option == 5):
            return
        if (option == 4):
            self._deleteUserPage()
        elif (option == 3):
            self._updateUserPage()
        elif (option == 2):
            self._createUserPage()
        elif (option == 1):
            self._findUserPage()
        else:
            self._showUserPage()

    def _showUserPage(self):
        print("Retrieving users ...")
        users = self.userManager.getAsync()

        clear_console()
        print("Results: \n")
        for i, user in enumerate(users):
            print(f"({i}) - {json.dumps(user)}")
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        pass

    def _findUserPage(self):
        print("Retrieving users ...")
        users = self.userManager.getAsync()
        print("Result may vary depending on your query (Leave it blank if you aren't sure) \n")
        
        username = input("What's it username: ")
        gender = input("What's it gender: ")
        age = int(input("What's it age: ") or 0)
        filtered_users = filter(lambda x: 
                                    (not username or x["username"] == username) and
                                    (not gender or x["gender"] == gender) and
                                    (not age or x["age"] == age), users)
        
        clear_console()
        print("Search results: \n")
        for i, user in enumerate(filtered_users):
            print(f"({i}) - {json.dumps(user)}")
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        
    def _createUserPage(self):
        newUsername = input("What's your name: ")
        newPassword = input("Please input your desirable password: ")
        newGender = input("What's your gender: ")
        newAge = int(input("What's your age: ") or 0)
    
        inputPermission = int(input("Register as? \n\n" \
                                    "[0] ADMIN \n" \
                                    "[1] Purchaser \n" \
                                    "[2] Inventory Checker \n\n" \
                                    "Select Item [0-2] (Default 0): ") or 0)
        
        if (inputPermission == 2):
            newPermission = self.permissionManager.findByRoleName("inventorychecker")
        elif (inputPermission == 1):
            newPermission = self.permissionManager.findByRoleName("purchaser")
        else:
            newPermission = self.permissionManager.findByRoleName("admin")

        self.userManager.createAsync({
                "username": newUsername,
                "password": newPassword,
                "gender": newGender,
                "age": newAge,
                "permissionId": newPermission["Id"]
            })
        input("\nUser created successfully ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")

    def _updateUserPage(self):
        userId = input("Which user would you like to update, Please input Id: ")
        user = self.userManager.findById(userId)

        if (user is None):
            showMessageAndRedirectToMainPage(self, message=f"User ({userId}) not found ...")

        print("Please fill up the form, except for those you want it to remain")
        updateUsername = input(f"New name: ") or user["username"]
        updatePassword = input("New password: ") or user["password"]
        updateGender = input("New gender: ") or user["gender"]
        updateAge = int(input("New age: ") or user["age"])

        inputPermission = int(input("Available Permissions \n\n" \
                                    "[0] ADMIN \n" \
                                    "[1] Purchaser \n" \
                                    "[2] Inventory Checker \n\n" \
                                    "Select Item [0-2] (Default 0): ") or 0)

        updatePermission = None
        if (inputPermission == 2):
            updatePermission = self.permissionManager.findByRoleName("inventorychecker")
        elif (inputPermission == 1):
            updatePermission = self.permissionManager.findByRoleName("purchaser")
        else:
            updatePermission = self.permissionManager.findByRoleName("admin")

        self.userManager.updateAsync( userId, {
                "username": updateUsername,
                "password": updatePassword,
                "gender": updateGender,
                "age": updateAge,
                "permissionId": updatePermission["Id"] or user["permissionId"]
        })
        showMessageAndRedirectToMainPage(self, message=f"User ({userId}) successfully updated ...")

    def _deleteUserPage(self):
        userId = input("Which user would you like to delete, Please input Id: ")
        self.userManager.deleteAsync(userId)
        showMessageAndRedirectToMainPage(self, message=f"User ({userId}) successfully removed ...")