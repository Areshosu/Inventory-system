from Services.Console import *
from Services.UserManager import UserManager
from Services.PermissionManager import PermissionManager
from Services.ItemManager import ItemManager
from Services.CategoryManager import CategoryManager

from Pages.ItemPage import ItemPage
from Pages.CategoryPage import CategoryPage
from Pages.UserPage import UserPage
from Pages.PermissionPage import PermissionPage

while True:
    clear_console()

    AuthenticatedUser = None
    CurrentUserPermission = None
    
    # Injecting modules
    itemManager = ItemManager()
    userManager = UserManager()
    permissionManager = PermissionManager()
    categoryManager = CategoryManager()
    
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
                        "[1] Manage Items \n" \
                        "[2] Manage Categories \n" \
                        "[3] Manage Permissions \n" \
                        "[4] Stock Taking \n" \
                        "[5] Search Item \n" \
                        "[6] View replenish Item Stock List \n" \
                        "[7] Replenish Item Stock List \n\n" \
                        "Select Item [0-7] (Default 0): ") or 0)

    # Management

    if (whatToDo is 1 and  CurrentUserPermission["canManageItem"] is True):
        ItemPage(itemManager)
        pass

    elif (whatToDo is 2 and  CurrentUserPermission["canManageCategory"] is True):
        CategoryPage(categoryManager)

    elif (whatToDo is 3 and  CurrentUserPermission["canManagePermission"] is True):
        PermissionPage(permissionManager)
        pass

    elif (whatToDo is 4 and  CurrentUserPermission["canStockTaking"] is True):
        pass

    elif (whatToDo is 5 and  CurrentUserPermission["canSearchItem"] is True):
        pass

    elif (whatToDo is 6 and  CurrentUserPermission["canViewReplenishStockList"] is True):
        pass

    elif (whatToDo is 7 and  CurrentUserPermission["canReplenishStock"] is True):
        pass
    
    elif (CurrentUserPermission["canManageUser"] is True):
        UserPage(userManager, permissionManager)
        pass    
    else:
        showMessageAndRestart("Insufficient Permission ...")