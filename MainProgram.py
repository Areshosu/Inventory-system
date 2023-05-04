from Services.Console import *
from Services.UserManager import UserManager
from Services.PermissionManager import PermissionManager
from Services.InventoryManager import InventoryManager

from Pages.UserPage import UserPage

while True:
    clear_console()

    AuthenticatedUser = None
    CurrentUserPermission = None
    
    # Injecting modules
    userManager = UserManager()
    permissionManager = PermissionManager()
    inventoryManager = InventoryManager()
    
    wantsToRegister = int(input("Would you like to login or register?\n" \
                            "[0] Login \n" \
                            "[1] Register \n\n" \
                            "Select Item [0-1] (Default 0): ") or 0)
    clear_console()
    
    if (wantsToRegister == 1):
        newUsername = input("What's your name: ")
        newPassword = input("Please input your desirable password: ")
        newGender = input("What's your gender: ")
        newAge = int(input("What's your age: "))
    
        inputPermission = int(input("Register as? \n\n" \
                                    "[0] ADMIN \n" \
                                    "[1] Purchaser \n" \
                                    "[2] Inventory Checker \n\n" \
                                    "Select Item [0-2] (Default 0): ") or 0)
        
        if (inputPermission == 2):
            newPermission = permissionManager.findByRoleName("inventorychecker")
        elif (inputPermission == 1):
            newPermission = permissionManager.findByRoleName("purchaser")
        else:
            newPermission = permissionManager.findByRoleName("admin")
        
        userManager.createAsync({
            "username": newUsername,
            "password": newPassword,
            "gender": newGender,
            "age": newAge,
            "permissionId": newPermission["Id"]
        })
    
        showMessageAndRestart("User created successfully, please proceed to login")
        pass
    
    print("Login \n")
    username = input("Username: ")
    password = input("Password: ")
    
    if (userManager.verifyLogin(username, password) is not True):
        showMessageAndRestart("Username or password is incorrect ...")

    AuthenticatedUser = userManager.findByUserName(username)
    CurrentUserPermission = permissionManager.findById(AuthenticatedUser["permissionId"])
    
    clear_console()
    whatToDo = int(input("How would you like to access this console? \n\n" \
                        "[0] Manage Users \n" \
                        "[1] Manage Item \n" \
                        "[2] Manage Permission \n" \
                        "[3] Stock Taking \n" \
                        "[4] Search Item \n" \
                        "[5] View replenish Item Stock List \n" \
                        "[6] Replenish Item Stock List \n\n" \
                        "Select Item [0-6] (Default 0): ") or 0)

    # Management

    if (whatToDo is 1 and  CurrentUserPermission["canManageItem"] is True):
        WhatToManage = int(input("How would you like to manage Items? \n\n" \
                        "[0] Show Item List \n" \
                        "[1] Find Item \n" \
                        "[2] Create Item \n" \
                        "[3] Delete Item \n\n" \
                        "Select Item [0-3] (Default 0): ") or 0)
        pass

    elif (whatToDo is 2 and  CurrentUserPermission["canManagePermission"] is True):
        WhatToManage = int(input("How would you like to manage Permissions? \n\n" \
                        "[0] Show Permission List \n" \
                        "[1] Find Permission \n" \
                        "[2] Create Permission \n" \
                        "[3] Delete Permission \n\n" \
                        "Select Item [0-3] (Default 0): ") or 0)
        pass

    elif (whatToDo is 3 and  CurrentUserPermission["canStockTaking"] is True):
        pass

    elif (whatToDo is 4 and  CurrentUserPermission["canSearchItem"] is True):
        pass

    elif (whatToDo is 5 and  CurrentUserPermission["canViewReplenishStockList"] is True):
        pass

    elif (whatToDo is 6 and  CurrentUserPermission["canReplenishStock"] is True):
        pass
    
    elif (CurrentUserPermission["canManageUser"] is True):
        UserPage(userManager, permissionManager)
        pass    
    else:
        showMessageAndRestart("Insufficient Permission ...")